

import xmltodict
import os
import random

from mongoengine import connect
from mongoengine import Document, IntField, FloatField, StringField

class Generar_parametros(object):

    def get_length(self,min,max):
        return round(random.uniform(min, max),0)

    def get_maxspeed(self,mu,sigma):
        return round(random.normalvariate(mu, sigma),2)
    
    def get_speedfactor(self,mu,sigma):
        return round(random.normalvariate(mu, sigma),2)

    def get_speeddev(self,mu,sigma):
        return round(random.normalvariate(mu, sigma),2)
    
    def get_accel(self,mu,sigma):
        return round(random.normalvariate(mu, sigma),2)

    def get_decel(self,mu,sigma):
        return round(random.normalvariate(mu, sigma),2)


class Parametros(Document):
    paramid = StringField(required=True)
    length = IntField(required=True)
    maxSpeed = FloatField(required=True,precision=2)
    speedFactor = FloatField(required=True,precision=2)
    speeddev= FloatField(required=True,precision=2)
    accel= FloatField(required=True,precision=2)
    decel= FloatField(required=True,precision=2)
    speed_out_average = FloatField(precision=2)
    
    def conectarse(self,db):
        if connect(db):
            print("conectado")
        else:
            print("error")        
        

def gen_vehicle(id,vClass):
    simulaciones = Parametros()
    generar_parametros=Generar_parametros()
    simulaciones.conectarse('simulacionesdb')
    simulaciones.paramid=id
    simulaciones.length=generar_parametros.get_length(1,3)
    length=simulaciones.length
    simulaciones.maxSpeed=generar_parametros.get_maxspeed(5,2)
    maxspeed=simulaciones.maxSpeed
    simulaciones.speedFactor=generar_parametros.get_speedfactor(1,1)
    speedfactor=simulaciones.speedFactor
    simulaciones.speeddev=generar_parametros.get_speeddev(1,1)
    speeddev=simulaciones.speeddev
    simulaciones.accel=generar_parametros.get_accel(2,1)
    accel=simulaciones.accel
    simulaciones.decel=generar_parametros.get_decel(2,1)
    decel=simulaciones.decel

    simulaciones.save()

    xmldata = {'additional':{
                'vType': {
                '@id':id,
                '@Vclass':vClass,
                '@length':length,
                '@maxSpeed':maxspeed,
                '@speedFactor':speedfactor,
                '@speedDev':speeddev,
                '@accel':accel,
                '@decel':decel,
                         }
                            }
                }

    print(xmltodict.unparse(xmldata,pretty=True))
    with open('example.xml', 'w') as result_file:
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
#routes("IbarraTriangleMap.net.xml","trips.trips.xml","example.xml","output.routes.xml")

gen_vehicle("type1","passenger")