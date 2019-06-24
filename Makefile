MYSQL_ARGS=--defaults-extra-file=mysql_args

read:
	mysql $(MYSQL_ARGS) images -e "drop table if exists observation"
	mysql $(MYSQL_ARGS) images -e "drop table if exists page"
	mysql $(MYSQL_ARGS) images -e "drop table if exists log"
	mysql $(MYSQL_ARGS) images -e "drop table if exists ship"
	mysql $(MYSQL_ARGS) images -e "drop table if exists archive"
	mysql $(MYSQL_ARGS) images < sql/archive.sql
	mysql $(MYSQL_ARGS) images < sql/ship.sql
	mysql $(MYSQL_ARGS) images < sql/log.sql
	mysql $(MYSQL_ARGS) images < sql/page.sql
	mysql $(MYSQL_ARGS) images < sql/observation.sql
api/head_date.txt:
	git log -1 --format="%ad" --date=format:"%Y-%m-%d" > "$@"

.PHONY: fetch_tablesorter
fetch_tablesorter:
	curl -Lo api/jquery.min.js \
		'https://code.jquery.com/jquery-3.2.1.min.js'
	curl -Lo api/jquery.tablesorter.js \
		'https://raw.githubusercontent.com/Mottie/tablesorter/master/js/jquery.tablesorter.js'
	curl -Lo api/tablesorter.css \
		'https://raw.githubusercontent.com/riceissa/tablesorter-bare-bones-theme/master/theme.css'

.PHONY: clean_tablesorter
clean_tablesorter:
	rm -f api/jquery.min.js
	rm -f api/jquery.tablesorter.js
	rm -f api/tablesorter.css

.PHONY: fetch_anchorjs
fetch_anchorjs:
	curl -Lo api/anchor.min.js \
		'https://raw.githubusercontent.com/bryanbraun/anchorjs/master/anchor.min.js'

.PHONY: clean_anchorjs
clean_anchorjs:
	rm -f api/anchor.min.js
