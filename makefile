all: install.pi


#Local Install for testing on desktop or laptop
install:
	mkdir -p /opt/mycroft/skills/skill-gpio
	cp -r * /opt/mycroft/skills/skill-gpio

#For removing the local install
remove:
	rm -rf /opt/mycroft/skills/skill-gpio

#For remote install to a Picroft image on a RPi
install.pi:
	scp -r * pi@192.168.205.115:/opt/mycroft/skills/skill-gpio

#For testing the install on the RPi
test.pi:
	ssh pi@192.168.205.115 python /opt/mycroft/skills/skill-gpio/GPIO.py

docs: docs/source/README.md
	cd docs && make clean && make html

docs/source/README.md: README.md
	cp README.md docs/source/README.md

#	pandoc --from=markdown --to=rst --output=docs/README.rst README.md

.PHONY: docs
