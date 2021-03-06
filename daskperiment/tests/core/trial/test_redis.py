from daskperiment.backend.redis import RedisBackend
from daskperiment.core.trial import NoSQLTrialManager
from daskperiment.testing import RedisCleanupMixin
from daskperiment.tests.core.trial.base import TrialManagerBase


class TestRedisTrialManager(TrialManagerBase, RedisCleanupMixin):

    backend = 'redis://localhost:6379/0'

    @property
    def trials(self):
        backend = RedisBackend('dummy', self.backend)
        return NoSQLTrialManager(backend=backend)

    def test_init(self):
        # test trial_id is properly initialized
        backend = RedisBackend('init', self.backend)
        t = NoSQLTrialManager(backend=backend)
        assert t.trial_id == 0
        assert not t.is_locked()
