psql -d postgresql://todoapp_user:tdapp8@localhost/todoapp_devel -c "INSERT INTO users VALUES(1, 'nikita', 'pbkdf2:sha256:150000\$VOMg755G\$273f7ce2ed9bf5aedce4793fbe7ebc1db9af1469858a2231daf5cbf23b68c3cf', 'some@mail.foo');"
psql -d postgresql://todoapp_user:tdapp8@localhost/todoapp_devel -c "INSERT INTO users VALUES(2, 'denchik', 'pbkdf2:sha256:150000\$wHwsgiLd\$6979f267446c0e3d2797c21006f9272c3e19d5c70925d87989983ab3826350d8', 'foo@bar.baz');"