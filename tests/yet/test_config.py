from yet.config.videoscache import VideosCache
from unittest import TestCase


class TestVideosCache(TestCase):
    TEST_URL = "_TestUrl_"

    def __init__(self):
        super().__init__()
        self.videos_cache = VideosCache()

    def test_videos_cache_add(self):
        self.videos_cache.add_to_cache(self.TEST_URL)
        c = self.videos_cache.contains(self.TEST_URL)
        self.assertTrue(c)

    def test_videos_cache_remove(self):
        self.videos_cache.delete(self.TEST_URL)
        c = self.videos_cache.contains(self.TEST_URL)
        self.assertFalse(c)
