#include <stdio.h>
#include <dlfcn.h>
#include <stdlib.h>
#include <vaccel.h>
#include <assert.h>

__attribute__((constructor))
void load_vaccel(void)
{
	printf("Loading libvaccel\n");
	void *dl = dlopen("libvaccel.so", RTLD_LAZY | RTLD_GLOBAL);
	if (!dl) {
		fprintf(stderr, "Could not open libvaccel\n");
		exit(1);
	}

	char *pname = getenv("PYTHON_VACCEL_PLUGIN");
	printf("Loading plugin %s\n", pname);
	void *plugin = dlopen(pname, RTLD_NOW);
	if (!plugin) {
		fprintf(stderr, "SKATA: %s\n", dlerror());
		exit(1);
	}

	struct vaccel_plugin **p;

	int (*register_plugin)(struct vaccel_plugin *) =
		dlsym(dl, "register_plugin");
	assert(register_plugin);

	p = dlsym(plugin, "vaccel_plugin");
	assert(p);

	int ret = register_plugin(*p);
	assert(!ret);

	ret = (*p)->info->init();
	assert(!ret);
}
