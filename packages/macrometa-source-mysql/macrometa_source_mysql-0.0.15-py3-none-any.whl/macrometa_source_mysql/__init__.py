# pylint: disable=missing-docstring,too-many-locals
import copy
import os

import pkg_resources
import pymysql
import singer
from c8connector import C8Connector, ValidationException, Sample, SchemaAttribute, Schema, SchemaAttributeType, \
    ConfigProperty, ConfigAttributeType
from prometheus_client import start_http_server, Counter, CollectorRegistry
from singer import metadata, get_logger
from singer import metrics
from singer.catalog import Catalog

from macrometa_source_mysql.connection import connect_with_backoff, MySQLConnection, MYSQL_ENGINE
from macrometa_source_mysql.discover_utils import discover_catalog, resolve_catalog
from macrometa_source_mysql.sample_data import modify_reserved_keys, fetch_samples
from macrometa_source_mysql.stream_utils import write_schema_message
from macrometa_source_mysql.sync_strategies import common, full_table, incremental, log_based

LOGGER = get_logger('macrometa_source_mysql')

REQUIRED_CONFIG_KEYS = [
    'host',
    'port',
    'user',
    'password',
    'database',
    'source_table',
]

region_label = os.getenv("GDN_FEDERATION", "NA")
tenant_label = os.getenv("GDN_TENANT", "NA")
fabric_label = os.getenv("GDN_FABRIC", "NA")
workflow_label = os.getenv("WORKFLOW_UUID", "NA")


class MySQLSourceConnector(C8Connector):
    """MySQLSourceConnector's C8Connector impl."""

    def name(self) -> str:
        """Returns the name of the connector."""
        return "MySQL"

    def package_name(self) -> str:
        """Returns the package name of the connector (i.e. PyPi package name)."""
        return "macrometa-source-mysql"

    def version(self) -> str:
        """Returns the version of the connector."""
        return pkg_resources.get_distribution('macrometa_source_mysql').version

    def type(self) -> str:
        """Returns the type of the connector."""
        return "source"

    def description(self) -> str:
        """Returns the description of the connector."""
        return "Source data from a MySQL database table."

    def validate(self, integration: dict) -> None:
        """Validate given configurations against the connector.
        If invalid, throw an exception with the cause.
        """
        try:
            config = self.get_config(integration)
            if config['replication_method'] not in ["FULL_TABLE", "LOG_BASED"]:
                raise Exception('Invalid replication method provided. It should be either FULL_TABLE or LOG_BASED.')
            mysql_conn = MySQLConnection(config, require_database=False)
            with connect_with_backoff(mysql_conn) as open_conn:
                try:
                    with open_conn.cursor() as cur:
                        # Check connection
                        cur.execute("SELECT VERSION()")
                        version = cur.fetchone()[0]
                        LOGGER.info("Server Version: %s", version)

                        # Check database existence
                        database_name = config.get('database')
                        cur.execute("SHOW DATABASES LIKE %s", (database_name,))
                        database_row = cur.fetchone()
                        if not database_row:
                            raise Exception(f"Database '{database_name}' does not exist.")

                        # Check table existence
                        table_name = config.get('source_table')
                        cur.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = %s AND "
                                    "table_name = %s", (database_name, table_name))
                        table_count = cur.fetchone()[0]
                        if table_count == 0:
                            raise Exception(f"Table '{table_name}' does not exist in database '{database_name}'.")
                except Exception as e:
                    raise e
        except Exception as e:
            raise ValidationException(e)

    def samples(self, integration: dict) -> list[Sample]:
        """Fetch sample data using the provided configurations."""
        try:
            self.validate(integration)
            config = self.get_config(integration)
            mysql_conn = MySQLConnection(config)
            catalog = do_discover(mysql_conn, config)
            results = []
            for stream in catalog.streams:
                s_attribs = []
                s_schema = stream.schema
                data = fetch_samples(mysql_conn, config, stream)[:10]
                # Appending _ to keys for preserving values of reserved keys in source data
                reserved_keys = ['_key', '_id', '_rev']
                if stream.metadata[0]['metadata'].get('table-key-properties'):
                    key_properties = stream.metadata[0]['metadata'].get('table-key-properties')
                    if key_properties[0] == '_key':
                        reserved_keys.remove('_key')
                s_schema.properties = modify_reserved_keys(s_schema.properties, reserved_keys)

                for k, v in s_schema.properties.items():
                    t = v.type[-1]
                    s_attribs.append(SchemaAttribute(k, self.get_attribute_type(t)))
                schema = Schema(stream.stream, s_attribs)
                results.append(Sample(
                    schema=schema,
                    data=data)
                )
        except Exception as e:
            LOGGER.info("Exception raised: %s", e)
            raise e
        return results

    def schemas(self, integration: dict) -> list[Schema]:
        """Get supported schemas using the given configurations."""
        try:
            self.validate(integration)
            config = self.get_config(integration)
            mysql_conn = MySQLConnection(config)
            catalog = do_discover(mysql_conn, config)
            results = []
            for stream in catalog.streams:
                s_attribs = []
                s_schema = stream.schema

                # Appending _ to keys for preserving values of reserved keys in source data
                reserved_keys = ['_key', '_id', '_rev']
                if stream.metadata[0]['metadata'].get('table-key-properties'):
                    key_properties = stream.metadata[0]['metadata'].get('table-key-properties')
                    if key_properties[0] == '_key':
                        reserved_keys.remove('_key')
                s_schema.properties = modify_reserved_keys(s_schema.properties, reserved_keys)

                for k, v in s_schema.properties.items():
                    t = v.type[-1]
                    s_attribs.append(SchemaAttribute(k, self.get_attribute_type(t)))
                results.append(Schema(stream.stream, s_attribs))
        except Exception as e:
            LOGGER.info("Exception raised: %s", e)
            raise e
        return results

    def reserved_keys(self) -> list[str]:
        """List of reserved keys for the connector."""
        return []

    @staticmethod
    def get_attribute_type(source_type: str) -> SchemaAttributeType:
        if source_type == 'string':
            return SchemaAttributeType.STRING
        elif source_type == 'integer':
            return SchemaAttributeType.LONG
        elif source_type == 'boolean':
            return SchemaAttributeType.BOOLEAN
        elif source_type == 'number':
            return SchemaAttributeType.DOUBLE
        else:
            return SchemaAttributeType.OBJECT

    def config(self) -> list[ConfigProperty]:
        """Get configuration parameters for the connector."""
        return [
            ConfigProperty('host', 'Host', ConfigAttributeType.STRING, True, False,
                           description='MySQL host.', placeholder_value='mysql_host'),
            ConfigProperty('port', 'Port', ConfigAttributeType.INT, True, False,
                           description='MySQL port.', default_value='3306'),
            ConfigProperty('user', 'Username', ConfigAttributeType.STRING, True, False,
                           description='MySQL username.', default_value='root'),
            ConfigProperty('password', 'Password', ConfigAttributeType.PASSWORD, True, False,
                           description='MySQL password.', placeholder_value='password'),
            ConfigProperty('database', 'Database Name', ConfigAttributeType.STRING, True, True,
                           description='MySQL database name.', default_value='mysql'),
            ConfigProperty('source_table', 'Source Table', ConfigAttributeType.STRING, True, True,
                           description='Source table to scan.', placeholder_value='my_table'),
            ConfigProperty('replication_method', 'Replication Method', ConfigAttributeType.STRING, True, True,
                           description='Choose from LOG_BASED, FULL_TABLE.', default_value='FULL_TABLE'),
            ConfigProperty('engine', 'Database Engine', ConfigAttributeType.STRING, False, False,
                           description='The database system (mysql or mariadb) being utilized for log event '
                                       'consumption.', default_value='mysql'),
            ConfigProperty('use_gtid', 'Use Global Transaction ID (GTID)', ConfigAttributeType.BOOLEAN, False, False,
                           description='When enabled, allows LOG_BASED to utilize Global Transaction ID (GTID) for '
                                       'log event tracking instead of binlog coordinates, with special handling for '
                                       'MariaDB\'s GTID implementation.', default_value='false'),
            ConfigProperty('internal_hostname', 'Internal Hostname', ConfigAttributeType.STRING, False, False,
                           description='Alternative host name for SSL certificate matching in cases where the '
                                       'connection host differs from the expected hostname, particularly useful for '
                                       'Google Cloud\'s self-signed certificates.',
                           placeholder_value='internal_hostname'),
            ConfigProperty('ssl', 'Use SSL', ConfigAttributeType.BOOLEAN, False, False,
                           description='Can be set to true to connect using SSL.',
                           default_value="false"),
            ConfigProperty('ssl_ca', 'SSL/TLS CA Certificate', ConfigAttributeType.FILE, False, False,
                           description='The file containing the Certificate Authority (CA) certificates for '
                                       'establishing secure SSL connections to the MySQL database.',
                           placeholder_value="my_ssl_ca"),
            ConfigProperty('ssl_cert', 'SSL/TLS Client Certificate', ConfigAttributeType.FILE, False, False,
                           description='The file containing the SSL certificate used for authentication when '
                                       'connecting securely to the MySQL database.',
                           placeholder_value="my_ssl_cert"),
            ConfigProperty('ssl_key', 'SSL/TLS Client Certificate Key', ConfigAttributeType.FILE, False, False,
                           description='The file containing the private key corresponding to the SSL certificate, '
                                       'required for secure authentication when connecting to the MySQL database '
                                       'using SSL.',
                           placeholder_value="my_ssl_key")
        ]

    def capabilities(self) -> list[str]:
        """Return the capabilities[1] of the connector.
        [1] https://docs.meltano.com/contribute/plugins#how-to-test-a-tap
        """
        return ['catalog', 'discover', 'state']

    @staticmethod
    def get_config(integration: dict) -> dict:
        try:
            return {
                # Required config keys
                'host': integration['host'],
                'port': integration['port'],
                'user': integration['user'],
                'password': integration['password'],
                'database': integration['database'],
                'source_table': integration['source_table'],
                'replication_method': integration.get('replication_method', "FULL_TABLE"),

                # Optional config keys
                'engine': integration.get('engine', "mysql"),
                'use_gtid': integration.get('use_gtid', False),
                'internal_hostname': integration.get('internal_hostname', ""),
                'ssl': integration.get('ssl', False),
                'ssl_ca': integration.get('ssl_ca', ""),
                'ssl_cert': integration.get('ssl_cert', ""),
                'ssl_key': integration.get('ssl_key', ""),

                # Un-exposed to the end-user
                # 'cursorclass': integration.get('cursorclass', "pymysql.cursors.SSCursor"),
                # 'server_id': integration.get('server_id', 1),
                # 'session_sqls': integration.get('session_sqls', DEFAULT_SESSION_SQLS),
            }
        except KeyError as e:
            raise ValidationException(f'Integration property `{e}` not found.') from e


def do_discover(mysql_conn, config):
    catalog = discover_catalog(mysql_conn, config.get('database'), config.get('source_table'))
    catalog.dump()
    return catalog


def log_engine(mysql_conn, catalog_entry):
    is_view = common.get_is_view(catalog_entry)
    database_name = common.get_database_name(catalog_entry)

    if is_view:
        LOGGER.info("Beginning sync for view %s.%s", database_name, catalog_entry.table)
    else:
        with connect_with_backoff(mysql_conn) as open_conn:
            with open_conn.cursor() as cur:
                cur.execute("""
                    SELECT engine
                      FROM information_schema.tables
                     WHERE table_schema = %s
                       AND table_name   = %s
                """, (database_name, catalog_entry.table))

                row = cur.fetchone()

                if row:
                    LOGGER.info("Beginning sync for %s table %s.%s",
                                row[0],
                                database_name,
                                catalog_entry.table)


def is_valid_currently_syncing_stream(selected_stream, config, state):
    stream_metadata = metadata.to_map(selected_stream.metadata)
    replication_method = stream_metadata.get((), {}).get('replication-method', config['replication_method'])

    if replication_method != 'LOG_BASED':
        return True

    if replication_method == 'LOG_BASED' and binlog_stream_requires_historical(selected_stream, state):
        return True

    return False


def binlog_stream_requires_historical(catalog_entry, state):
    log_file = singer.get_bookmark(state,
                                   catalog_entry.tap_stream_id,
                                   'log_file')

    log_pos = singer.get_bookmark(state,
                                  catalog_entry.tap_stream_id,
                                  'log_pos')

    gtid = singer.get_bookmark(state,
                               catalog_entry.tap_stream_id,
                               'gtid')

    max_pk_values = singer.get_bookmark(state,
                                        catalog_entry.tap_stream_id,
                                        'max_pk_values')

    last_pk_fetched = singer.get_bookmark(state,
                                          catalog_entry.tap_stream_id,
                                          'last_pk_fetched')

    if ((log_file and log_pos) or gtid) and (not max_pk_values and not last_pk_fetched):
        return False

    return True


def get_non_binlog_streams(mysql_conn, catalog, config, state):
    """
    Returns the Catalog of data we're going to sync for all SELECT-based
    streams (i.e. INCREMENTAL, FULL_TABLE, and LOG_BASED that require a historical
    sync). LOG_BASED streams that require a historical sync are inferred from lack
    of any state.

    Using the Catalog provided from the input file, this function will return a
    Catalog representing exactly which tables and columns that will be emitted
    by SELECT-based syncs. This is achieved by comparing the input Catalog to a
    freshly discovered Catalog to determine the resulting Catalog.

    The resulting Catalog will include the following any streams marked as
    "selected" that currently exist in the database. Columns marked as "selected"
    and those labeled "automatic" (e.g. primary keys and replication keys) will be
    included. Streams will be prioritized in the following order:
      1. currently_syncing if it is SELECT-based
      2. any streams that do not have state
      3. any streams that do not have a replication method of LOG_BASED

    """
    discovered = discover_catalog(mysql_conn, config.get('database'), config.get('source_table'))

    # Filter catalog to include only selected streams
    selected_streams = list(filter(common.stream_is_selected, catalog.streams))
    streams_with_state = []
    streams_without_state = []

    for stream in selected_streams:
        stream_metadata = metadata.to_map(stream.metadata)
        replication_method = stream_metadata.get((), {}).get('replication-method', config['replication_method'])
        stream_state = state.get('bookmarks', {}).get(stream.tap_stream_id)

        if not stream_state:
            if replication_method == 'LOG_BASED':
                LOGGER.info("LOG_BASED stream %s requires full historical sync", stream.tap_stream_id)

            streams_without_state.append(stream)
        elif stream_state and replication_method == 'LOG_BASED' and binlog_stream_requires_historical(stream, state):
            is_view = common.get_is_view(stream)

            if is_view:
                raise Exception(
                    f"Unable to replicate stream({stream.stream}) with binlog because it is a view.")

            LOGGER.info("LOG_BASED stream %s will resume its historical sync", stream.tap_stream_id)

            streams_with_state.append(stream)
        elif stream_state and replication_method != 'LOG_BASED':
            streams_with_state.append(stream)

    # If the state says we were in the middle of processing a stream, skip
    # to that stream. Then process streams without prior state and finally
    # move onto streams with state (i.e. have been synced in the past)
    currently_syncing = singer.get_currently_syncing(state)

    # prioritize streams that have not been processed
    ordered_streams = streams_without_state + streams_with_state

    if currently_syncing:
        currently_syncing_stream = list(filter(
            lambda s: s.tap_stream_id == currently_syncing and is_valid_currently_syncing_stream(s, config, state),
            streams_with_state))

        non_currently_syncing_streams = list(filter(lambda s: s.tap_stream_id != currently_syncing, ordered_streams))

        streams_to_sync = currently_syncing_stream + non_currently_syncing_streams
    else:
        # prioritize streams that have not been processed
        streams_to_sync = ordered_streams

    return resolve_catalog(discovered, streams_to_sync)


def get_binlog_streams(mysql_conn, catalog, config, state):
    discovered = discover_catalog(mysql_conn, config.get('database'), config.get('source_table'))

    selected_streams = list(filter(common.stream_is_selected, catalog.streams))
    binlog_streams = []

    for stream in selected_streams:
        stream_metadata = metadata.to_map(stream.metadata)
        replication_method = stream_metadata.get((), {}).get('replication-method', config['replication_method'])

        # When LOG_BASED is selected, since we are syncing FULL_TABLE and the LOG_BASED immediately, changing the
        # `if replication_method == 'LOG_BASED' and not binlog_stream_requires_historical(stream, state):` to following;
        if replication_method == 'LOG_BASED':
            binlog_streams.append(stream)

    return resolve_catalog(discovered, binlog_streams)


def do_sync_incremental(mysql_conn, catalog_entry, config, state, columns):
    LOGGER.info("Stream %s is using incremental replication", catalog_entry.stream)

    md_map = metadata.to_map(catalog_entry.metadata)
    replication_key = md_map.get((), {}).get('replication-key')

    if not replication_key:
        raise Exception(
            f"Cannot use INCREMENTAL replication for table ({catalog_entry.stream}) without a replication key.")

    write_schema_message(catalog_entry=catalog_entry,
                         bookmark_properties=[replication_key])

    incremental.sync_table(mysql_conn, catalog_entry, config, state, columns)

    singer.write_message(singer.StateMessage(value=copy.deepcopy(state)))


# pylint: disable=too-many-arguments
def do_sync_historical_binlog(mysql_conn, catalog_entry, config, state, columns, use_gtid: bool, engine: str):
    log_based.verify_binlog_config(mysql_conn)

    if use_gtid and engine == MYSQL_ENGINE:
        log_based.verify_gtid_config(mysql_conn)

    is_view = common.get_is_view(catalog_entry)

    if is_view:
        raise Exception(f"Unable to replicate stream({catalog_entry.stream}) with binlog because it is a view.")

    log_file = singer.get_bookmark(state,
                                   catalog_entry.tap_stream_id,
                                   'log_file')

    log_pos = singer.get_bookmark(state,
                                  catalog_entry.tap_stream_id,
                                  'log_pos')

    gtid = None
    if use_gtid:
        gtid = singer.get_bookmark(state,
                                   catalog_entry.tap_stream_id,
                                   'gtid')

    max_pk_values = singer.get_bookmark(state,
                                        catalog_entry.tap_stream_id,
                                        'max_pk_values')

    write_schema_message(catalog_entry)

    stream_version = common.get_stream_version(catalog_entry.tap_stream_id, state)

    if max_pk_values and ((use_gtid and gtid) or (log_file and log_pos)):
        LOGGER.info("Resuming initial full table sync for LOG_BASED stream %s", catalog_entry.tap_stream_id)
        full_table.sync_table(mysql_conn, catalog_entry, config, state, columns, stream_version)
    else:
        LOGGER.info("Performing initial full table sync for LOG_BASED stream %s", catalog_entry.tap_stream_id)

        state = singer.write_bookmark(state,
                                      catalog_entry.tap_stream_id,
                                      'initial_binlog_complete',
                                      False)

        current_log_file, current_log_pos = log_based.fetch_current_log_file_and_pos(mysql_conn)

        current_gtid = None
        if use_gtid:
            current_gtid = log_based.fetch_current_gtid_pos(mysql_conn, engine)

        state = singer.write_bookmark(state,
                                      catalog_entry.tap_stream_id,
                                      'version',
                                      stream_version)

        if full_table.pks_are_auto_incrementing(mysql_conn, catalog_entry):
            # We must save log_file, log_pos, gtid across FULL_TABLE syncs when using
            # an incrementing PK
            state = singer.write_bookmark(state,
                                          catalog_entry.tap_stream_id,
                                          'log_file',
                                          current_log_file)

            state = singer.write_bookmark(state,
                                          catalog_entry.tap_stream_id,
                                          'log_pos',
                                          current_log_pos)

            if current_gtid:
                state = singer.write_bookmark(state,
                                              catalog_entry.tap_stream_id,
                                              'gtid',
                                              current_gtid)

            full_table.sync_table(mysql_conn, catalog_entry, config, state, columns, stream_version)

        else:
            full_table.sync_table(mysql_conn, catalog_entry, config, state, columns, stream_version)
            state = singer.write_bookmark(state,
                                          catalog_entry.tap_stream_id,
                                          'log_file',
                                          current_log_file)

            state = singer.write_bookmark(state,
                                          catalog_entry.tap_stream_id,
                                          'log_pos',
                                          current_log_pos)

            if current_gtid:
                state = singer.write_bookmark(state,
                                              catalog_entry.tap_stream_id,
                                              'gtid',
                                              current_gtid)


def do_sync_full_table(mysql_conn, catalog_entry, config, state, columns):
    LOGGER.info("Stream %s is using full table replication", catalog_entry.stream)

    write_schema_message(catalog_entry)

    stream_version = common.get_stream_version(catalog_entry.tap_stream_id, state)

    full_table.sync_table(mysql_conn, catalog_entry, config, state, columns, stream_version)

    # Prefer initial_full_table_complete going forward
    singer.clear_bookmark(state, catalog_entry.tap_stream_id, 'version')

    state = singer.write_bookmark(state,
                                  catalog_entry.tap_stream_id,
                                  'initial_full_table_complete',
                                  True)

    singer.write_message(singer.StateMessage(value=copy.deepcopy(state)))


def sync_non_binlog_streams(mysql_conn, non_binlog_catalog, config, state):
    LOGGER.info(f"Started syncing FULL_TABLE.")
    use_gtid = config['use_gtid']
    engine = config['engine']
    for catalog_entry in non_binlog_catalog.streams:
        columns = list(catalog_entry.schema.properties.keys())

        if not columns:
            LOGGER.warning('There are no columns selected for stream %s, skipping it.', catalog_entry.stream)
            continue

        state = singer.set_currently_syncing(state, catalog_entry.tap_stream_id)

        # Emit a state message to indicate that we've started this stream
        singer.write_message(singer.StateMessage(value=copy.deepcopy(state)))

        md_map = metadata.to_map(catalog_entry.metadata)

        replication_method = md_map.get((), {}).get('replication-method', config['replication_method'])

        database_name = common.get_database_name(catalog_entry)

        with metrics.job_timer('sync_table') as timer:
            timer.tags['database'] = database_name
            timer.tags['table'] = catalog_entry.table

            log_engine(mysql_conn, catalog_entry)

            if replication_method == 'INCREMENTAL':
                do_sync_incremental(mysql_conn, catalog_entry, config, state, columns)
            elif replication_method == 'LOG_BASED':
                do_sync_historical_binlog(mysql_conn, catalog_entry, config, state, columns, use_gtid, engine)
            elif replication_method == 'FULL_TABLE':
                do_sync_full_table(mysql_conn, catalog_entry, config, state, columns)
            else:
                raise Exception("only INCREMENTAL, LOG_BASED, and FULL TABLE replication methods are supported")

    state = singer.set_currently_syncing(state, None)
    singer.write_message(singer.StateMessage(value=copy.deepcopy(state)))
    LOGGER.info(f"Completed syncing FULL_TABLE.")


def sync_binlog_streams(mysql_conn, binlog_catalog, config, state):
    if binlog_catalog.streams:
        LOGGER.info(f"Started syncing LOG_BASED.")
        for stream in binlog_catalog.streams:
            write_schema_message(stream)

        with metrics.job_timer('sync_binlog'):
            binlog_streams_map = log_based.generate_streams_map(binlog_catalog.streams)
            log_based.sync_binlog_stream(mysql_conn, config, binlog_streams_map, state)


def do_sync(mysql_conn, config, catalog, state):
    config['use_gtid'] = config.get('use_gtid', False)
    config['engine'] = config.get('engine', MYSQL_ENGINE).lower()
    non_binlog_catalog = get_non_binlog_streams(mysql_conn, catalog, config, state)
    binlog_catalog = get_binlog_streams(mysql_conn, catalog, config, state)

    sync_non_binlog_streams(mysql_conn, non_binlog_catalog, config, state)
    sync_binlog_streams(mysql_conn, binlog_catalog, config, state)


def log_server_params(mysql_conn):
    with connect_with_backoff(mysql_conn) as open_conn:
        try:
            with open_conn.cursor() as cur:
                cur.execute('''
                SELECT VERSION() as version,
                       @@session.wait_timeout as wait_timeout,
                       @@session.innodb_lock_wait_timeout as innodb_lock_wait_timeout,
                       @@session.max_allowed_packet as max_allowed_packet,
                       @@session.interactive_timeout as interactive_timeout''')
                row = cur.fetchone()
                LOGGER.info('Server Parameters: ' +
                            'version: %s, ' +
                            'wait_timeout: %s, ' +
                            'innodb_lock_wait_timeout: %s, ' +
                            'max_allowed_packet: %s, ' +
                            'interactive_timeout: %s',
                            *row)
            with open_conn.cursor() as cur:
                cur.execute('''
                show session status where Variable_name IN ('Ssl_version', 'Ssl_cipher')''')
                rows = cur.fetchall()
                mapped_row = {r[0]: r[1] for r in rows}
                LOGGER.info(
                    'Server SSL Parameters(blank means SSL is not active): [ssl_version: %s], [ssl_cipher: %s]',
                    mapped_row['Ssl_version'], mapped_row['Ssl_cipher'])

        except pymysql.err.InternalError as exc:
            LOGGER.warning("Encountered error checking server params. Error: (%s) %s", *exc.args)


def main_impl():
    # Create a custom CollectorRegistry
    registry_package = CollectorRegistry()
    ingest_errors = Counter('ingest_errors', 'Total number of errors during ingestion',
                            ['region', 'tenant', 'fabric', 'workflow'], registry=registry_package)
    LOGGER.info("MySQL source is starting the metrics server.")
    start_http_server(8000, registry=registry_package)

    try:
        args = singer.utils.parse_args(REQUIRED_CONFIG_KEYS)

        mysql_conn = MySQLConnection(args.config)
        log_server_params(mysql_conn)

        if args.discover:
            do_discover(mysql_conn, args.config)
        elif args.catalog:
            state = args.state or {}
            do_sync(mysql_conn, args.config, args.catalog, state)
        elif args.properties:
            catalog = Catalog.from_dict(args.properties)
            state = args.state or {}
            do_sync(mysql_conn, args.config, catalog, state)
        else:
            LOGGER.info("No properties were selected")
    except Exception as e:
        LOGGER.warn("Exception raised: %s", e)
        ingest_errors.labels(region_label, tenant_label, fabric_label, workflow_label).inc()
        raise e


def main():
    try:
        main_impl()
    except Exception as exc:
        LOGGER.critical(exc)
        raise exc
