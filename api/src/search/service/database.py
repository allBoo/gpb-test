from sqlalchemy import union_all, select, literal_column, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from search.data.dto.results import SearchResults, SearchItem
from search.service import SearchService
from storage.data.models.maillog import Log, Message


class DatabaseSearchService(SearchService):
    def __init__(self, connection: AsyncSession):
        self.connection = connection

    async def search_by_email(self, email: str, limit: int = 100) -> SearchResults:
        """
        Execute search by email
        :param email:
        :param limit:
        :return:
        """

        """
        Used query:
        
        WITH ids AS (
            SELECT
                int_id
            FROM
                log
            WHERE address = ':email'
        
            UNION
        
            SELECT
                int_id
            FROM
                message
            WHERE str ilike '%:email%'
        ),
        data as (
            SELECT
                int_id,
                created,
                str,
                'LOG' as type
            FROM
                log
            WHERE int_id IN (SELECT * FROM ids)
        
            UNION ALL
        
            SELECT
                int_id,
                created,
                str,
                'MESSAGE' as type
            FROM
                message
            WHERE int_id IN (SELECT * FROM ids)
        )
        SELECT
            *
        FROM
            data
        ORDER BY
            int_id, created
        """

        ids_cte = union_all(
            select(Log.int_id).where(Log.address == email),
            select(Message.int_id).where(Message.str.ilike(f"%{email}%"))
        ).cte("ids")

        data_cte = union_all(
            select(
                Log.int_id,
                Log.created,
                Log.str,
                literal_column("'LOG'").label("type")
            ).where(Log.int_id.in_(select(ids_cte.c.int_id))),
            select(
                Message.int_id,
                Message.created,
                Message.str,
                literal_column("'MESSAGE'").label("type")
            ).where(Message.int_id.in_(select(ids_cte.c.int_id)))
        ).cte("data")

        query = select(data_cte).order_by(data_cte.c.int_id, data_cte.c.created).limit(limit)
        count_query = select(func.count().label("total")).select_from(data_cte)

        result = await self.connection.execute(query)
        items = [SearchItem.model_validate(item, from_attributes=True) for item in result.fetchall()]

        total_result = await self.connection.execute(count_query)
        total = total_result.scalar()

        return SearchResults(items=items, total=total)
