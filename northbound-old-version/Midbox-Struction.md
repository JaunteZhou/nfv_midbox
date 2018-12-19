# 中间件架构

## 北向RESTful API架构设计

###### NorthRESTfulAPI.py

先定义父类class NorthRESTfulAPI(Resource, Abort)，作为北向接口类的模板类，其中定义了4种接口，分别为get查询，post添加，put更新，delete删除，本设计中，几乎不使用put更新项。

再从父类继承定义与具体接口绑定的类，包括：

- (Resource_CloudNode, '/resource/cloudnode/<service_node_id>')
- (Resources_VM_Flavor, '/resources/vm/flavor/<flavor_id>')
- (Resources_VM_Flavor, '/resources/vm/flavor')

- (Resources_VM_Image, '/resources/vm/image/<vm_image_id>')
- (Resources_VM_Image, '/resources/vm/image/<image_file_name>')
- (Resources_Container_Image, '/resources/container/image/<container_image_id>')
- (Resources_Container_Image, '/resources/container/image/<image_file_name>')
- (Resources_SecurityFunction, '/resources/security-function/<security_function_id>')

- (Running_CloudNode_FlowTable, '/running/cloudnode/<service_node_id>/flow-table')

- (Running_VM_instance, '/running/vm/instance/<vm_id>')

- (Running_Container, '/running/container/<container_id>')

- (Running_CloudNode, '/running/cloudnode/<service_node_id>')

- (Running_Switch, '/running/switch/<switch_id>')

对应负责接收各种北向请求并组合相应返回数据，处理北向请求通过调用**中心单元类CenterUnit中的proc方法函数**完成。



## 中心单元架构设计

###### CenterUnit.py

承接北向RESTful API，对指定数据进行相关的转化，并下发给南向服务代理完成请求的具体实现。

中心单元类class CenterUnit(object)

定义该类的对象时，需要提供一个字符串列表作为参数，指明需要创建的**南向服务代理**的种类，本设计中包括OpenStack，Swarm，OpenFlow，SQLite四个服务代理。

该类中包含一个方法函数proc(self, method, south_agent, item = "", para)，向北向RESTful API提供唯一接口接收北向请求，被调用时需要4个参数：

- method：字符串，GET，POST，DELETE，PUT等代表北向请求类型；
- south_agent：字符串，OPENSTACK，SWARM，OPENFLOW等代表所需的南向服务代理的类型；
- item：字符串，IMAGE，FLAVOR，INSTANCE，CONTAINER等代表请求所对应的资源元素类型；
- para：字典，字典的key值为字符串，包含相应参数的字典。

方法函数proc中根据前3个参数，确定将要调用的南向服务代理的相关接口，并将第4个参数para传递给南向服务代理；或者其中特定的一些情况下，需要对参数进行一定的转换，则调用该类的私有函数完成。

其中，私有函数有：

__show_security_function(self, para)

__delete_security_function(self, para)

等。在这些私有函数中，需要通过数据库服务代理的查询等功能，完成对参数的转化。



## 南向服务代理

### OpenStack服务代理

###### OpenStackAgent.py

通过shade库，完成对OpenStack云计算平台的增删改查服务。主要功能包括对云节点node、虚拟机镜像image、虚拟机实例类型flavor、虚拟机实例instance的查询、添加、删除等服务功能。接收参数为字典。

### Swarm服务代理

###### SwarmAgent.py



### OpenFlow服务代理

###### OpenFlowAgent.py



### SQLite服务代理

###### SQLiteAgent.py