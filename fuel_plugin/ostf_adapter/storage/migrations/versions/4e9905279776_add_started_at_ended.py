#    Copyright 2013 Mirantis, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""Add started_at , ended_at on TestRun model

Revision ID: 4e9905279776
Revises: 12340edd992d
Create Date: 2013-07-04 12:10:49.219213

"""

# revision identifiers, used by Alembic.
revision = '4e9905279776'
down_revision = '12340edd992d'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('test_runs',
                  sa.Column('started_at', sa.DateTime(), nullable=True))
    op.add_column('test_runs',
                  sa.Column('ended_at', sa.DateTime(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('test_runs', 'ended_at')
    op.drop_column('test_runs', 'started_at')
    ### end Alembic commands ###
