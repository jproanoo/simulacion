

import xmltodict
import os
import random


class Generar_parametros(object):

    def get_length(self,mu,sigma):
        return random.normalvariate(mu, sigma)

    def get_maxspeed(self,mu,sigma):
        return random.normalvariate(mu, sigma)
    
    def get_speedfactor(self,mu,sigma):
        return random.normalvariate(mu, sigma)

    def get_speeddev(self,mu,sigma):
        return random.normalvariate(mu, sigma)
    
    def get_accel(self,mu,sigma):
        return random.normalvariate(mu, sigma)

    def get_decel(self,mu,sigma):
        return random.normalvariate(mu, sigma)


def gen_vehicle(id,vClass):
    
    generar_parametros=Generar_parametros()

    xmldata = {'additional':{
                'vType': {
                '@id':id,
                '@Vclass':vClass,
                '@length':generar_parametros.get_length(3,5),
                '@maxSpeed':generar_parametros.get_maxspeed(5,8),
                '@speedFactor':generar_parametros.get_speedfactor(0,1),
                '@speedDev':generar_parametros.get_speeddev(2,3),
                '@accel':generar_parametros.get_accel(0,1),
                '@decel':generar_parametros.get_decel(0,1),
                         }
                            }
                }

    print(xmltodict.unparse(xmldata,pretty=True))
    with open('example.xml', 'a') as result_file:
        result_file.write(xmltodict.unparse(xmldata))



def network(grid,carriles,longitud,salida):
    os.system('netgenerate --grid  --grid.number={0} -L={1} --grid.length={2} --output-file={3}' .format(str(grid), str(carriles), str(longitud),str(salida)))
    return
    

def trips(net, id,add):

    os.system('python3 $SUMO_HOME/tools/randomTrips.py -n {0} --trip-attributes={1} --additional-file {2} --edge-permission passenger'.format(net,id,add))
    print("trips generated")
    return

def routes(red,trips,add,output):
    print(add)
    os.system('duarouter -n {0} --route-files {1} --additional-files {2} -o {3}'.format(red,trips,add,output))
    # duarouter -n IbarraTriangleMap.net.xml --route-files trips.trips.xml -o routas.rou.xml
    print("rutas created")
    return

def simulacion():
    #<configuration>
	#<input>
	#	<net-file value="IbarraTriangleMap.net.xml"/>
	#	<route-files value="trips.trips.xml"/>
	#	<additional-files value="add-vtype.xml"/>
	#</input>

	#<time>
	#	<begin value="0"/>	
	#</time>
	
	#<output>
	#	<summary-output value="Summary.xml" />
	#	<emission-output value="Emissions.xml" />
	#</output>

	#<report>
	#	<xml-validation value="never"/>
	#	<duration-log.disable value="true"/>
	#	<duration-log.statistics value="true"/>
	#	<no-step-log value="true"/>
	#	<device.emissions.probability value="1.0"/>
	#</report>
#</configuration>
    pass

my_str = "type=\\\"type1\\\""

#trips("IbarraTriangleMap.net.xml",my_str,"example.xml")
routes("IbarraTriangleMap.net.xml","trips.trips.xml","example.xml","output.routes.xml")

#gen_vehicle("type1","passenger")