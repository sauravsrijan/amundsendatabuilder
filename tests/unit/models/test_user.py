import unittest

from databuilder.models.neo4j_csv_serde import RELATION_START_KEY, RELATION_START_LABEL, RELATION_END_KEY, \
    RELATION_END_LABEL, RELATION_TYPE, RELATION_REVERSE_TYPE

from databuilder.models.user import User


class TestUser(unittest.TestCase):

    def setUp(self):
        # type: () -> None
        super(TestUser, self).setUp()
        self.user = User(first_name='test_first',
                         last_name='test_last',
                         name='test_first test_last',
                         email='test@email.com',
                         github_username='github_test',
                         team_name='test_team',
                         employee_type='FTE',
                         manager_email='test_manager@email.com',
                         slack_id='slack',
                         is_active=True,
                         updated_at=1)

    def test_get_user_model_key(self):
        # type: () -> None
        user_email = User.get_user_model_key(email=self.user.email)
        self.assertEquals(user_email, '{email}'.format(email='test@email.com'))

    def test_create_nodes(self):
        # type: () -> None
        nodes = self.user.create_nodes()
        self.assertEquals(len(nodes), 1)

    def test_create_relation(self):
        # type: () -> None
        relations = self.user.create_relation()
        self.assertEquals(len(relations), 1)

        start_key = '{email}'.format(email='test@email.com')
        end_key = '{email}'.format(email='test_manager@email.com')

        relation = {
            RELATION_START_KEY: start_key,
            RELATION_START_LABEL: User.USER_NODE_LABEL,
            RELATION_END_KEY: end_key,
            RELATION_END_LABEL: User.USER_NODE_LABEL,
            RELATION_TYPE: User.USER_MANAGER_RELATION_TYPE,
            RELATION_REVERSE_TYPE: User.MANAGER_USER_RELATION_TYPE
        }

        self.assertTrue(relation in relations)
