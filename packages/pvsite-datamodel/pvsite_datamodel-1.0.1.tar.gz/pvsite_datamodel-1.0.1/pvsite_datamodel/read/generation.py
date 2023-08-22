"""Read pv generation functions."""
import logging
import uuid
from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session, contains_eager

from pvsite_datamodel.sqlmodels import (
    GenerationSQL,
    SiteGroupSiteSQL,
    SiteGroupSQL,
    SiteSQL,
    UserSQL,
)

logger = logging.getLogger(__name__)


def get_pv_generation_by_user_uuids(
    session: Session,
    start_utc: Optional[datetime] = None,
    end_utc: Optional[datetime] = None,
    user_uuids: Optional[List[str]] = None,
) -> List[GenerationSQL]:
    """Get the generation data by user uuids.

    :param session: database session
    :param start_utc: search filters >= on 'datetime_utc'. Can be None
    :param end_utc: search filters < on 'datetime_utc'. Can be None
    :param user_uuids: optional list of user uuids
    :return:list of pv yields.
    """
    # start main query
    query = session.query(GenerationSQL)
    query = query.join(SiteSQL)

    # Filter by time interval
    if start_utc is not None:
        query = query.filter(
            GenerationSQL.start_utc >= start_utc,
        )

    if end_utc is not None:
        query = query.filter(
            GenerationSQL.end_utc < end_utc,
        )

    if user_uuids is not None:
        query = query.join(SiteGroupSiteSQL)
        query = query.join(SiteGroupSQL)
        query = query.join(UserSQL)
        query = query.filter(UserSQL.user_uuid.in_(user_uuids))

    query = query.order_by(
        SiteSQL.site_uuid,
        GenerationSQL.start_utc,
    )

    # get all results
    generations: List[GenerationSQL] = query.all()

    return generations


def get_pv_generation_by_sites(
    session: Session,
    start_utc: Optional[datetime] = None,
    end_utc: Optional[datetime] = None,
    site_uuids: Optional[List[uuid.UUID]] = None,
) -> List[GenerationSQL]:
    """Get the generation data by site.

    :param session: database session
    :param start_utc: search filters >= on 'datetime_utc'
    :param end_utc: search fileters < on 'datetime_utc'
    :param site_uuids: optional list of site uuids
    :return: list of pv yields
    """
    # start main query
    query = session.query(GenerationSQL)
    query = query.join(SiteSQL)

    # Filter by time interval
    if start_utc is not None:
        query = query.filter(
            GenerationSQL.start_utc >= start_utc,
        )

    if end_utc is not None:
        query = query.filter(
            GenerationSQL.end_utc < end_utc,
        )

    if site_uuids is not None:
        query = query.filter(SiteSQL.site_uuid.in_(site_uuids))

    query = query.order_by(SiteSQL.site_uuid, GenerationSQL.start_utc)

    # make sure this is all loaded
    query = query.options(contains_eager(GenerationSQL.site)).populate_existing()

    # get all results
    generations: List[GenerationSQL] = query.all()

    return generations
