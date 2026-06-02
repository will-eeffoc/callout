# Generated migration to remove half stars from ratings

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chipin', '0004_alter_review_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.DecimalField(choices=[(1, '★☆☆☆☆'), (2, '★★☆☆☆'), (3, '★★★☆☆'), (4, '★★★★☆'), (5, '★★★★★')], decimal_places=1, max_digits=2),
        ),
    ]
