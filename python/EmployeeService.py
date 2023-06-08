from concurrent import futures
import logging

import grpc
import EmployeeService_pb2
import EmployeeService_pb2_grpc
import const

empDB=[
 {
 'id':101,
 'name':'Saravanan S',
 'title':'Technical Leader'
 'salary': 300
 },
 {
 'id':201,
 'name':'Rajkumar P',
 'title':'Sr Software Engineer'
 'salary':400
 }
 ]

class EmployeeServer(EmployeeService_pb2_grpc.EmployeeServiceServicer):

  def CreateEmployee(self, request, context):
    dat = {
    'id':request.id,
    'name':request.name,
    'title':request.title
    'salary':request.salary
    }
    empDB.append(dat)
    return EmployeeService_pb2.StatusReply(status='OK')

  def GetEmployeeDataFromID(self, request, context):
    usr = [ emp for emp in empDB if (emp['id'] == request.id) ]
    return EmployeeService_pb2.EmployeeData(id=usr[0]['id'], name=usr[0]['name'], title=usr[0]['title'], salary=usr[0]['salary'])
  def UpdateEmployeeSalary(self, request, context):
    usr = [emp for emp in empDB if (emp['id'] == request.id)]
    usr[0]['salary'] = request.salary
    return EmployeeService_pb2.StatusReply(status='OK')

  def UpdateEmployeeTitle(self, request, context):
    usr = [ emp for emp in empDB if (emp['id'] == request.id) ]
    usr[0]['title'] = request.title
    return EmployeeService_pb2.StatusReply(status='OK')

  def DeleteEmployee(self, request, context):
    usr = [ emp for emp in empDB if (emp['id'] == request.id) ]
    if len(usr) == 0:
      return EmployeeService_pb2.StatusReply(status='NOK')
    else:
      empDB.remove(usr[0])
      return EmployeeService_pb2.StatusReply(status='OK')

  def ListAllEmployees(self, request, context):
    list = EmployeeService_pb2.EmployeeDataList()
    for item in empDB:
      emp_data = EmployeeService_pb2.EmployeeData(id=item['id'], name=item['name'], title=item['title'], salary=item['salary'])
      list.employee_data.append(emp_data)
    return list

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    EmployeeService_pb2_grpc.add_EmployeeServiceServicer_to_server(EmployeeServer(), server)
    server.add_insecure_port('[::]:'+const.PORT)
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
