from typing import Optional, List, Dict, Any
from pydantic import BaseModel

from depot_service.models.abfss_depot import AbfssDepot
from depot_service.models.big_query_depot import BigQueryDepot
from depot_service.models.elastic_search_depot import ElasticSearchDepot
from depot_service.models.eventhub_depot import EventhubDepot
from depot_service.models.file_depot import FileDepot
from depot_service.models.gcs_depot import GCSDepot
from depot_service.models.htttp_depot import HttpDepot
from depot_service.models.jdbc_depot import JdbcDepot
from depot_service.models.kafka_depot import KafkaDepot
from depot_service.models.mongo_db_depot import MongoDBDepot
from depot_service.models.mysql_depot import MysqlDepot
from depot_service.models.open_search_depot import OpenSearchDepot
from depot_service.models.oracle_depot import OracleDepot
from depot_service.models.postgres_depot import PostgresDepot
from depot_service.models.presto_depot import PrestoDepot
from depot_service.models.pulsar_depot import PulsarDepot
from depot_service.models.redis_depot import RedisDepot
from depot_service.models.redshift_depot import RedshiftDepot
from depot_service.models.s3_depot import S3Depot
from depot_service.models.snowflake_depot import SnowflakeDepot
from depot_service.models.wasbs_depot import WasbsDepot


class DepotRequest(BaseModel):
    type: str
    external: Optional[bool]
    owners: List[str]
    description: Optional[str]
    meta: Optional[Dict[str, Any]]
    source: Optional[str]
    abfss: Optional[AbfssDepot]
    bigquery: Optional[BigQueryDepot]
    elasticsearch: Optional[ElasticSearchDepot]
    eventhub: Optional[EventhubDepot]
    file: Optional[FileDepot]
    gcs: Optional[GCSDepot]
    http: Optional[HttpDepot]
    jdbc: Optional[JdbcDepot]
    kafka: Optional[KafkaDepot]
    mongodb: Optional[MongoDBDepot]
    mysql: Optional[MysqlDepot]
    opensearch: Optional[OpenSearchDepot]
    oracle: Optional[OracleDepot]
    postgresql: Optional[PostgresDepot]
    presto: Optional[PrestoDepot]
    pulsar: Optional[PulsarDepot]
    redis: Optional[RedisDepot]
    redshift: Optional[RedshiftDepot]
    s3: Optional[S3Depot]
    snowflake: Optional[SnowflakeDepot]
    wasbs: Optional[WasbsDepot]
