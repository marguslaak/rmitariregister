# Generated by Django 5.0.4 on 2024-04-26 12:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data_storage', '0005_remove_enterprisegroup_party_remove_legalperson_name_and_more'),
    ]

    operations = [
        migrations.RunSQL(
            sql='alter table data_storage_enterprisegroup drop constraint data_storage_enterpr_group_head_id_92fa9180_fk_data_stor;'
                'alter table data_storage_enterprisegroup add constraint data_storage_enterpr_group_head_id_92fa9180_fk_data_stor foreign key (group_head_id) references data_storage_party (id) on delete cascade on update cascade;',
            reverse_sql='alter table data_storage_enterprisegroup drop constraint data_storage_enterpr_group_head_id_92fa9180_fk_data_stor;'
                        'alter table data_storage_enterprisegroup add constraint data_storage_enterpr_group_head_id_92fa9180_fk_data_stor foreign key (group_head_id) references data_storage_party (id);'
        ),
        migrations.RunSQL(
            sql='alter table data_storage_physicalperson drop constraint data_storage_physica_party_id_d3949966_fk_data_stor;'
                'alter table data_storage_physicalperson add constraint data_storage_physica_party_id_d3949966_fk_data_stor foreign key (party_id) references data_storage_party (id) on delete cascade on update cascade;',
            reverse_sql='alter table data_storage_physicalperson drop constraint data_storage_physica_party_id_d3949966_fk_data_stor;'
                        'alter table data_storage_physicalperson add constraint data_storage_physica_party_id_d3949966_fk_data_stor foreign key (party_id) references data_storage_party (id);'
        ),
        migrations.RunSQL(
            sql='alter table data_storage_legalperson drop constraint data_storage_legalpe_party_id_14376fe8_fk_data_stor;'
                'alter table data_storage_legalperson add constraint data_storage_legalpe_party_id_14376fe8_fk_data_stor foreign key (party_id) references data_storage_party (id) on delete cascade on update cascade;',
            reverse_sql='alter table data_storage_legalperson drop constraint data_storage_legalpe_party_id_14376fe8_fk_data_stor;'
                        'alter table data_storage_legalperson add constraint data_storage_legalpe_party_id_14376fe8_fk_data_stor foreign key (party_id) references data_storage_party (id);'
        ),
        migrations.RunSQL(
            sql='alter table data_storage_assets drop constraint data_storage_assets_legal_person_id_46265410_fk_data_stor;'
                'alter table data_storage_assets add constraint data_storage_assets_legal_person_id_46265410_fk_data_stor foreign key (legal_person_id) references data_storage_legalperson (id) on delete cascade on update cascade;',
            reverse_sql='alter table data_storage_assets drop constraint data_storage_assets_legal_person_id_46265410_fk_data_stor;'
                        'alter table data_storage_assets add constraint data_storage_assets_legal_person_id_46265410_fk_data_stor foreign key (legal_person_id) references data_storage_legalperson (id);'
        ),
        migrations.RunSQL(
            sql='alter table data_storage_ownership drop constraint data_storage_ownersh_child_party_id_b27d9f25_fk_data_stor;'
                'alter table data_storage_ownership add constraint data_storage_ownersh_child_party_id_b27d9f25_fk_data_stor foreign key (child_party_id) references data_storage_party (id) on delete cascade on update cascade;',
            reverse_sql='alter table data_storage_ownership drop constraint data_storage_ownersh_child_party_id_b27d9f25_fk_data_stor;'
                        'alter table data_storage_ownership add constraint data_storage_ownersh_child_party_id_b27d9f25_fk_data_stor foreign key (child_party_id) references data_storage_party (id);'
        ),
        migrations.RunSQL(
            sql='alter table data_storage_ownership drop constraint data_storage_ownersh_parent_party_id_94622456_fk_data_stor;'
                'alter table data_storage_ownership add constraint data_storage_ownersh_parent_party_id_94622456_fk_data_stor foreign key (parent_party_id) references data_storage_party (id) on delete cascade on update cascade;',
            reverse_sql='alter table data_storage_ownership drop constraint data_storage_ownersh_parent_party_id_94622456_fk_data_stor;'
                        'alter table data_storage_ownership add constraint data_storage_ownersh_parent_party_id_94622456_fk_data_stor foreign key (parent_party_id) references data_storage_party (id);'
        ),
        migrations.RunSQL(
            sql='alter table data_storage_ownership drop constraint data_storage_ownersh_enterprise_group_id_e8fbc3fa_fk_data_stor;'
                'alter table data_storage_ownership add constraint data_storage_ownersh_enterprise_group_id_e8fbc3fa_fk_data_stor foreign key (enterprise_group_id) references data_storage_enterprisegroup (id) on delete cascade on update cascade;',
            reverse_sql='alter table data_storage_ownership drop constraint data_storage_ownersh_enterprise_group_id_e8fbc3fa_fk_data_stor;'
                        'alter table data_storage_ownership add constraint data_storage_ownersh_enterprise_group_id_e8fbc3fa_fk_data_stor foreign key (enterprise_group_id) references data_storage_enterprisegroup (id);'
        )
    ]