from nptracer.gengaLoader import GengaLoader
from nptracer.changaLoader import ChangaLoader
from nptracer.dataAnalyzer import DataAnalyzer
from matplotlib import pyplot as plt

loader = GengaLoader('../simdata/genga/')
analyzer = DataAnalyzer(loader.read_snaps(), 0.08)
print(analyzer.ids_final)

id = 20


time, prop = analyzer.get_time_prop(id, 'm')

fig, ax = plt.subplots()
ax.plot(time, prop, '.-')
ax.set_xlabel('Time'); ax.set_ylabel('Property'); ax.set_title(f'ID: {id}')
ax.set_xscale('log')
plt.show()

# time, max_prop = analyzer.get_time_max('m')

# fig, ax = plt.subplots()
# ax.plot(time, max_prop, '.-')
# ax.set_xlabel('Time'); ax.set_ylabel('Max Property'); 

# ax.set_xscale('log');# ax.set_yscale('log')
# plt.show()


# df_id = analyzer.data.query(f'id == 0')

x =30
print(x)

#loader = ChangaLoader('simdata/changa/')
#all_snaps = loader.read_snaps()