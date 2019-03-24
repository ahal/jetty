import os

from ..command import Command


class CacheClearCommand(Command):
    """
    Clears poetry's cache.

    cache:clear
        { cache : The name of the cache to clear. }
        { --all : Clear all caches. }
    """

    def handle(self):
        from cachy import CacheManager
        from poetry.locations import CACHE_DIR
        from poetry.utils._compat import Path

        cache = self.argument("cache")

        parts = cache.split(":")
        root = parts[0]

        base_cache = Path(CACHE_DIR) / "cache" / "repositories"
        cache_dir = base_cache / root

        try:
            cache_dir.relative_to(base_cache)
        except ValueError:
            raise ValueError("{} is not a valid repository cache".format(root))

        cache = CacheManager(
            {
                "default": parts[0],
                "serializer": "json",
                "stores": {parts[0]: {"driver": "file", "path": str(cache_dir)}},
            }
        )

        if len(parts) == 1:
            if not self.option("all"):
                raise RuntimeError(
                    "Add the --all option if you want to clear all "
                    "{} caches".format(parts[0])
                )

            if not os.path.exists(str(cache_dir)):
                self.line("No cache entries for {}".format(parts[0]))
                return 0

            # Calculate number of entries
            entries_count = 0
            for path, dirs, files in os.walk(str(cache_dir)):
                entries_count += len(files)

            delete = self.confirm(
                "<question>Delete {} entries?</>".format(entries_count)
            )
            if not delete:
                return 0

            cache.flush()
        elif len(parts) == 2:
            raise RuntimeError(
                "Only specifying the package name is not yet supported. "
                "Add a specific version to clear"
            )
        elif len(parts) == 3:
            package = parts[1]
            version = parts[2]

            if not cache.has("{}:{}".format(package, version)):
                self.line("No cache entries for {}:{}".format(package, version))
                return 0

            delete = self.confirm("Delete cache entry {}:{}".format(package, version))
            if not delete:
                return 0

            cache.forget("{}:{}".format(package, version))
        else:
            raise ValueError("Invalid cache key")
