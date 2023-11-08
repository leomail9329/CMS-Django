# Generated by Django 1.10.8 on 2018-01-03 19:50
from __future__ import unicode_literals

from django.db import migrations, router

from . import IrreversibleMigration


def unpublish_never_published_pages(apps, schema_editor):
    """
        publisher_public__isnull=True,
    )

    for page in never_published_pages.distinct():
        page.title_set.update(
            published=False,
            publisher_state=1,
        )
        draft_pages.filter(pk=page.pk).update(
            publication_date=None,
            publication_end_date=None,
        )


def set_page_nodes(apps, schema_editor):
    Page = apps.get_model('cms', 'Page')
    TreeNode = apps.get_model('cms', 'TreeNode')
    db_alias = schema_editor.connection.alias
    draft_pages = Page.objects.using(db_alias).filter(publisher_is_draft=True)
    public_pages = Page.objects.using(db_alias).filter(publisher_is_draft=False)
    nodes_by_path = {node.path: node for node in TreeNode.objects.all()}

    for draft_page in draft_pages:
        draft_page.node = nodes_by_path[draft_page.path]
        draft_page.save(update_fields=['node'])

        if draft_page.publisher_public_id:
            public_pages.filter(pk=draft_page.publisher_public_id).update(node=draft_page.node)


class Migration(IrreversibleMigration):

    dependencies = [
        ('cms', '0018_create_pagenode'),
    ]

    operations = [
        migrations.RunPython(unpublish_never_published_pages),
        migrations.RunPython(set_page_nodes),
    ]

    def apply(self, project_state, schema_editor, collect_sql=False):
        model = project_state.apps.get_model('cms', 'page')
        if not all(op.allow_migrate_model(schema_editor.connection.alias, model) for op in self.operations):
            return project_state

        connection = schema_editor.connection
        if router.allow_migrate(connection.alias, 'cms', model_name='cms_page'):
            column_names = [
                column.name for column in
                connection.introspection.get_table_description(connection.cursor(), 'cms_page')
            ]

            if 'migration_0018_control' in column_names:
                # The new 0018 migration has been applied
                return super(Migration, self).apply(project_state, schema_editor, collect_sql)

            # The old 0018 migration was applied
            # Move the project state forward without actually running
            # any of the operations against the database.
            for operation in self.operations:
                operation.state_forwards(self.app_label, project_state)
        return project_state