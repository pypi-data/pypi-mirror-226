#  Copyright 2023 Nyria
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program. If not, see <https://www.gnu.org/licenses/>.

from typing import Union

from ory.asyncio.async_pool import AsyncPool
from ory.ext.exceptions import PoolAlreadyExistsException, PriorityAlreadyExistsException
from ory.registry.pool_registry import PoolRegistry
from ory.states.permission import Permission


class AsyncRegistryHandler:
    """
    The registry handler is used to create, delete and get pools. It fully supports async.
    """
    @staticmethod
    async def create_new_pool(pool: AsyncPool, override: bool = False) -> None:
        """
        Create new service pool

        Attributes:
        ------------
        :param pool: The pool to create
        :param override: If the pool should be overriden if it already exists
        :return: None
        """

        if await pool.get_name() in PoolRegistry.pool_storage and not override:
            raise PoolAlreadyExistsException("Service pool already exists")

        for registered_pool in PoolRegistry.pool_storage.values():
            if await registered_pool.get_priority() == await pool.get_priority() and pool.get_priority() != 0:
                raise PriorityAlreadyExistsException("Service pool with same priority already exists")

        if await pool.get_name() in PoolRegistry.pool_storage and not override:
            raise PoolAlreadyExistsException("Service pool already exists")

        PoolRegistry.pool_storage[await pool.get_name()] = pool

    @staticmethod
    async def create_new_pools(pools: list[AsyncPool], override: bool = False) -> None:
        """
        Create multiple new service pools
        :param pools: The pools to create
        :param override: If the pools should be overriden if they already exists
        :return: None
        """

        for pool in pools:
            await AsyncRegistryHandler.create_new_pool(pool, override)

    @staticmethod
    async def delete_pool(pool: AsyncPool) -> None:
        """
        Delete a pool by its name

        Attributes:
        ------------
        :param pool: The pool to delete
        :return: None
        ------------
        """

        if await pool.get_permission() != Permission.ALL:
            raise PermissionError("Missing permission to delete pool")

        del PoolRegistry.pool_storage[await pool.get_name()]

    @staticmethod
    async def get_all_pools() -> list:
        """
        Get all pools

        Attributes:
        ------------
        :return: All pools
        ------------
        """

        return [pool for pool in PoolRegistry.pool_storage.values()]

    @staticmethod
    async def get_pool_by_name(name: str) -> Union[AsyncPool, None]:
        """
        Get a pool by its name

        Attributes:
        ------------
        :param name: The name of the pool.
        :return: The pool
        ------------
        """

        for pool in PoolRegistry.pool_storage.values():
            if await pool.get_name() == name.lower():
                return pool

        return None

    @staticmethod
    async def get_pool_by_priority(priority: int) -> Union[list[AsyncPool], AsyncPool, None]:
        """
        Get a pool by its priority

        Attributes:
        ------------
        :param priority: The priority of the pool.
        :return: The pool
        ------------
        """

        if priority == 0:
            return [pool for pool in PoolRegistry.pool_storage.values() if await pool.get_priority() == 0]

        for pool in PoolRegistry.pool_storage.values():
            if await pool.get_priority() == priority:
                return pool

        return None

    @staticmethod
    async def get_standard_pools() -> list[AsyncPool]:
        """
        Get all standard pools

        Attributes:
        ------------
        :return: All standard pools
        ------------
        """

        return [pool for pool in PoolRegistry.pool_storage.values() if await pool.get_priority() == 0]
