MYSQL_ARGS=--defaults-extra-file=user/mysql_args

read:
	mysql $(MYSQL_ARGS) images -e "drop table if exists observation"
	mysql $(MYSQL_ARGS) images -e "drop table if exists image"
	mysql $(MYSQL_ARGS) images -e "drop table if exists document"
	mysql $(MYSQL_ARGS) images -e "drop table if exists platform"
	mysql $(MYSQL_ARGS) images -e "drop table if exists archive"
	mysql $(MYSQL_ARGS) images < schema/archive.sql
	mysql $(MYSQL_ARGS) images < schema/platform.sql
	mysql $(MYSQL_ARGS) images < schema/document.sql
	mysql $(MYSQL_ARGS) images < schema/image.sql
	mysql $(MYSQL_ARGS) images < schema/observation.sql
api/head_date.txt:
	git document -1 --format="%ad" --date=format:"%Y-%m-%d" > "$@"

.PHONY: describe
describe:
	mysql $(MYSQL_ARGS) images -e "describe archive;"
	mysql $(MYSQL_ARGS) images -e "describe platform;"
	mysql $(MYSQL_ARGS) images -e "describe document;"
	mysql $(MYSQL_ARGS) images -e "describe image;"
	mysql $(MYSQL_ARGS) images -e "describe observation;"

# .PHONY: fetch_tablesorter
# fetch_tablesorter:
# 	curl -Lo api/jquery.min.js \
# 		'https://code.jquery.com/jquery-3.2.1.min.js'
# 	curl -Lo api/jquery.tablesorter.js \
# 		'https://raw.githubusercontent.com/Mottie/tablesorter/master/js/jquery.tablesorter.js'
# 	curl -Lo api/tablesorter.css \
# 		'https://raw.githubusercontent.com/riceissa/tablesorter-bare-bones-theme/master/theme.css'

# .PHONY: clean_tablesorter
# clean_tablesorter:
# 	rm -f api/jquery.min.js
# 	rm -f api/jquery.tablesorter.js
# 	rm -f api/tablesorter.css

# .PHONY: fetch_anchorjs
# fetch_anchorjs:
# 	curl -Lo api/anchor.min.js \
# 		'https://raw.githubusercontent.com/bryanbraun/anchorjs/master/anchor.min.js'

# .PHONY: clean_anchorjs
# clean_anchorjs:
# 	rm -f api/anchor.min.js
