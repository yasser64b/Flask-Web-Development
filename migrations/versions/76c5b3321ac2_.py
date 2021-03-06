"""empty message

Revision ID: 76c5b3321ac2
Revises: 
Create Date: 2021-02-20 20:38:47.266544

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '76c5b3321ac2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('beams',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('blog_post_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.Text(), nullable=True),
    sa.Column('Node1', sa.Float(), nullable=True),
    sa.Column('Node2', sa.Float(), nullable=True),
    sa.Column('support1_dof', sa.Text(), nullable=True),
    sa.Column('support1_loc', sa.Float(), nullable=True),
    sa.Column('support2_dof', sa.Text(), nullable=True),
    sa.Column('support2_loc', sa.Float(), nullable=True),
    sa.Column('I', sa.Float(), nullable=True),
    sa.Column('E', sa.Float(), nullable=True),
    sa.Column('unit', sa.Text(), nullable=True),
    sa.Column('pointLoad', sa.Float(), nullable=True),
    sa.Column('pointLoadLoc', sa.Float(), nullable=True),
    sa.Column('momentLoad', sa.Float(), nullable=True),
    sa.Column('momentLoadLoc', sa.Float(), nullable=True),
    sa.Column('distLoadBeg', sa.Float(), nullable=True),
    sa.Column('distLoadBegLoc', sa.Float(), nullable=True),
    sa.Column('distLoadEnd', sa.Float(), nullable=True),
    sa.Column('distLoadEndLoc', sa.Float(), nullable=True),
    sa.Column('max_disp', sa.Float(), nullable=True),
    sa.Column('min_disp', sa.Float(), nullable=True),
    sa.Column('disp0L', sa.Float(), nullable=True),
    sa.Column('disp05L', sa.Float(), nullable=True),
    sa.Column('dispL', sa.Float(), nullable=True),
    sa.Column('disp_max_x', sa.Float(), nullable=True),
    sa.Column('disp_min_x', sa.Float(), nullable=True),
    sa.Column('max_moment', sa.Float(), nullable=True),
    sa.Column('min_moment', sa.Float(), nullable=True),
    sa.Column('moment0L', sa.Float(), nullable=True),
    sa.Column('moment05L', sa.Float(), nullable=True),
    sa.Column('momentL', sa.Float(), nullable=True),
    sa.Column('max_shear', sa.Float(), nullable=True),
    sa.Column('min_shear', sa.Float(), nullable=True),
    sa.Column('shear0L', sa.Float(), nullable=True),
    sa.Column('shear05L', sa.Float(), nullable=True),
    sa.Column('shearL', sa.Float(), nullable=True),
    sa.Column('R1', sa.Float(), nullable=True),
    sa.Column('R2', sa.Float(), nullable=True),
    sa.Column('beam_img', sa.Text(), nullable=True),
    sa.Column('result_img', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('mycolumns',
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('blog_post_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.Text(), nullable=True),
    sa.Column('unit', sa.Text(), nullable=True),
    sa.Column('E', sa.Float(), nullable=True),
    sa.Column('Node1', sa.Float(), nullable=True),
    sa.Column('Node2', sa.Float(), nullable=True),
    sa.Column('I', sa.Float(), nullable=True),
    sa.Column('support1_dof', sa.Text(), nullable=True),
    sa.Column('support1_loc', sa.Float(), nullable=True),
    sa.Column('support2_dof', sa.Text(), nullable=True),
    sa.Column('support2_loc', sa.Float(), nullable=True),
    sa.Column('pointLoad', sa.Float(), nullable=True),
    sa.Column('pointLoadLoc', sa.Float(), nullable=True),
    sa.Column('K_factor', sa.Float(), nullable=True),
    sa.Column('buckling_load1', sa.Float(), nullable=True),
    sa.Column('buckling_load2', sa.Float(), nullable=True),
    sa.Column('buckling_load3', sa.Float(), nullable=True),
    sa.Column('result_img', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('supports1',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sup1', sa.Text(), nullable=True),
    sa.Column('code1', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('supports2',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sup2', sa.Text(), nullable=True),
    sa.Column('code2', sa.Text(), nullable=True),
    sa.Column('sup1_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('trusses',
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('blog_post_id', sa.Integer(), nullable=True),
    sa.Column('truss_type', sa.Text(), nullable=True),
    sa.Column('unit', sa.Text(), nullable=True),
    sa.Column('E', sa.Float(), nullable=True),
    sa.Column('A', sa.Float(), nullable=True),
    sa.Column('numSpans', sa.Float(), nullable=True),
    sa.Column('span_width', sa.Float(), nullable=True),
    sa.Column('truss_height', sa.Float(), nullable=True),
    sa.Column('support1_dof', sa.Text(), nullable=True),
    sa.Column('support1_node', sa.Integer(), nullable=True),
    sa.Column('support2_dof', sa.Text(), nullable=True),
    sa.Column('support2_node', sa.Integer(), nullable=True),
    sa.Column('pointLoad1x', sa.Float(), nullable=True),
    sa.Column('pointLoad1y', sa.Float(), nullable=True),
    sa.Column('pointLoadNode1', sa.Integer(), nullable=True),
    sa.Column('pointLoad2x', sa.Float(), nullable=True),
    sa.Column('pointLoad2y', sa.Float(), nullable=True),
    sa.Column('pointLoadNode2', sa.Integer(), nullable=True),
    sa.Column('pointLoad3x', sa.Float(), nullable=True),
    sa.Column('pointLoad3y', sa.Float(), nullable=True),
    sa.Column('pointLoadNode3', sa.Integer(), nullable=True),
    sa.Column('result_img', sa.Text(), nullable=True),
    sa.Column('maxDispy', sa.Float(), nullable=True),
    sa.Column('maxDispNodey', sa.Float(), nullable=True),
    sa.Column('minDispy', sa.Float(), nullable=True),
    sa.Column('minDispNodey', sa.Float(), nullable=True),
    sa.Column('maxDispx', sa.Float(), nullable=True),
    sa.Column('maxDispNodex', sa.Float(), nullable=True),
    sa.Column('minDispx', sa.Float(), nullable=True),
    sa.Column('minDispNodex', sa.Float(), nullable=True),
    sa.Column('R1x', sa.Float(), nullable=True),
    sa.Column('R1y', sa.Float(), nullable=True),
    sa.Column('R2x', sa.Float(), nullable=True),
    sa.Column('R2y', sa.Float(), nullable=True),
    sa.Column('maxForce', sa.Float(), nullable=True),
    sa.Column('maxForceElem', sa.Float(), nullable=True),
    sa.Column('minForce', sa.Float(), nullable=True),
    sa.Column('minForceElem', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('profile_image', sa.String(length=20), nullable=False),
    sa.Column('email', sa.String(length=64), nullable=True),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_table('blog_post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('title', sa.String(length=140), nullable=False),
    sa.Column('text', sa.Text(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('blog_post')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_table('trusses')
    op.drop_table('supports2')
    op.drop_table('supports1')
    op.drop_table('mycolumns')
    op.drop_table('beams')
    # ### end Alembic commands ###
