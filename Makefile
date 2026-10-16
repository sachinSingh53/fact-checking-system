.PHONY: install backend-install frontend-install backend-dev frontend-dev backend-check frontend-check check

install: backend-install frontend-install

backend-install:
	$(MAKE) -C backend install

frontend-install:
	pnpm --dir frontend install

backend-dev:
	$(MAKE) -C backend dev

frontend-dev:
	pnpm --dir frontend dev

backend-check:
	$(MAKE) -C backend check

frontend-check:
	pnpm --dir frontend check

check: backend-check frontend-check
