
import time, os, json, requests

#cpu
def fibonacci(x):
    a, b = 0, 1
    n = 0
    while n < x:
        a, b = b, a+b
        n += 1
    return a

#memory
def concatena_Str():
    a = ''
    for i in range(8192000):
        a += 'a'

#disk
def create_File():
    file = open('test01.txt','w')
    until = 65536
    for j in range(until):
        file.write("In meteorology, a cloud is a visible mass of liquid droplets or frozen crystals made of water or various chemicals suspended in the atmosphere above the surface of a planetary body.[1] These suspended particles are also known as aerosols and are studied in the cloud physics branch of meteorology.Terrestrial cloud formation is the result of air in Earthzs atmosphere becoming saturated due to either or both of two processes; cooling of the air and adding water vapor. With sufficient saturation, precipitation will fall to the surface; an exception is virga, which evaporates before reaching the surface.Clouds in the troposphere, the atmospheric layer closest to Earthzs surface, have Latin names due to the universal adaptation of Luke Howardzs nomenclature. It was introduced in December 1802 and became the basis of a modern international system that classifies these tropospheric aerosols into several physical forms or categories, then cross-classifies them into families of low-, middle- and high-atage according to cloud-base altitude range above Earthzs surface. Clouds with significant vertical extent occupying more than one atage are often considered a separate family. One physical form shows free-convective upward growth into low or vertical heaps of cumulus. Other forms appear as non-convective layered sheets like low stratus, and as limited-convective rolls or ripples as with stratocumulus. Both of these layered forms have middle- and high-atage variants identified respectively by the prefixes alto- and cirro-. Thin fibrous wisps of cirrus are a physical form found only at high altitudes of the tropopshere. In the case of clouds with vertical extent, prefixes are used whenever necessary to express variations or complexities in their physical structures. These include cumulo- for complex highly convective vertical nimbus storm clouds, and nimbo- for thick stratiform layers with sufficient vertical depth to produce moderate to heavy precipitation. This process of cross-classification produces ten basic genus-types or genera, most of which can be subdivided into species and varieties. Synoptic surface weather observations use code numbers to record and report any type of tropospheric cloud visible at scheduled observation times based on its height and physical appearance.While a majority of clouds form in Earthzs troposphere, there are occasions when they can be observed at much higher altitudes in the stratosphere and mesosphere. Clouds that form above the troposphere have common names for their main types, but are sub-classified alpha-numerically rather than with the elaborate system of Latin names given to cloud types in the troposphere. These three main atmospheric layers that can produce clouds, along with the lowest part of the cloudless thermosphere, are collectively known as the homosphere. Above this lies the heterosphere (which includes the rest of the thermosphere and the exosphere) that marks the transition to outer space. Clouds have been observed on other planets and moons within the Solar System, but, due to their different temperature characteristics, they are often composed of other substances such as methane, ammonia, and sulfuric acid as well as water.The Bergeron classification is the most widely accepted form of air mass classification.. Air mass classification involves three letters. The first letter describes its moisture properties, with c used for continental air masses (dry) and m for maritime air masses (moist). The second letter describes the thermal characteristic of its source region: T for tropical, P for polar, A for arctic or Antarctic, M for monsoon, E for equatorial, and S for superior air (dry air formed by significant upward motion in the atmosphere). The third letter is used to designate the stability of the atmosphere. If the air mass is colder than the ground below it, it is labeled k. If the air mass is warmer than the ground below it, it is labeled w.[3] Fronts separate air masses of different types or origins, and are located along troughs of lower pressure.[4]A surface weather the.")
    file.close()

    file2 = open('test01.txt', 'r')
    while True:
        if(file2.readline()==''):
            break
    file2.close()
 
    os.remove('test01.txt')

def run(turns=30):
    cpu = []
    memory = []
    disk = []
    
    for i in range(turns):
        t1 = int(round(time.time() * 1000))
        fibonacci(500000)
        cpu.append(int(round(time.time() * 1000))-t1)

        t1 = int(round(time.time() * 1000))
        concatena_Str()
        memory.append(int(round(time.time() * 1000))-t1)

        t1 = int(round(time.time() * 1000))
        create_File()
        disk.append(int(round(time.time() * 1000))-t1)

    return {'cpu':cpu, 'memory':memory, 'disk':disk}

arq = open('benchmarking_data.txt', 'w')
arq.write(json.dumps(run()))
arq.close()

while True:
    try:
        r = requests.get('http://0.0.0.0:5151/change_status')
        if r.status_code == 200:
            break
    except:
        time.sleep(1)
        continue
