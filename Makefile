#!/usr/bin/make -f
##
# Helper functions for Service management.
##

##
# Services - web_index
##

web_index/site: web_index/themes/aamod/theme.toml web_index/themes/mainroad/theme.toml
	cd web_index && hugo --minify -d site

%/theme.toml:
	git submodule update --init --recursive $*

web_index-browse: web_index/site
	cd web_index && sensible-browser site/index.html

web_index-run:
	cd web_index && hugo server --disableFastRender

##
# Testing
##

test: test-debian test-ubuntu test-rocky

test-%: tpod_%
	podman run --rm -it \
		--hostname service01-test \
		-v "$(PWD):/srv/ansible" \
		tpod_$* /srv/ansible/test/docker/test.sh


##
# Container
##

# Create a container for testing
tpod_%:
	podman build -t $@ \
		-f test/docker/create.$*

# Log in to a container named "tpod_%"
login-%: tpod_%
	podman run --rm -it \
		--hostname service01-test \
		-v "$(PWD):/srv/ansible" \
		tpod_$* /bin/bash


##
# Cleanup
##

# Purge podman and other testing artifacts
clean: cleanpod-tpod_debian cleanpod-tpod_ubuntu cleanpod-tpod_rocky
	podman system prune -f
	# hugo
	$(RM) -r web_index/.hugo_site web_index/resources web_index/site

# Delete a container if it exists
cleanpod-%:
	@if [ -n "$(findstring $*,$(shell podman images))" ]; then \
		podman rmi $*; \
	fi
