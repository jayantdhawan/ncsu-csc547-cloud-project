CREATE TABLE user_storage_grp (user_id varchar(255), storage_grp_id int, date_timestamp timestamp with time zone);
ALTER TABLE user_storage_grp ADD PRIMARY KEY(user_id,storage_grp_id);
GRANT ALL PRIVILEGES ON TABLE user_storage_grp TO transuser;

CREATE TABLE storage_grp_cinder(storage_grp_id int,cinder_id varchar(255), date_timestamp timestamp with time zone);
ALTER TABLE storage_grp_cinder ADD PRIMARY KEY(storage_grp_id,cinder_id);
GRANT ALL PRIVILEGES ON TABLE storage_grp_cinder TO transuser;

