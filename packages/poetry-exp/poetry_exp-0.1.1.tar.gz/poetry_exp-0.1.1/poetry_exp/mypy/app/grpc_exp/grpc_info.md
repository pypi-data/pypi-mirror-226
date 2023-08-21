https://grpc.io/docs/what-is-grpc/introduction/
In gRPC, a client application can directly call a method on a server application on a different machine as
if it were a local object, making it easier for you to create distributed applications and services. 
As in many RPC systems, gRPC is based around the idea of defining a service, specifying the methods
that can be called remotely with their parameters and return types. On the server side, the server
implements this interface and runs a gRPC server to handle client calls. On the client side,
the client has a stub (referred to as just a client in some languages) that provides the same methods as the server.

gRPC clients and servers can run and talk to each other in a variety of environments - from servers inside
Google to your own desktop - and can be written in any of gRPC’s supported languages. So,
for example, you can easily create a gRPC server in Java with clients in Go, Python, or Ruby. 
In addition, the latest Google APIs will have gRPC versions of their interfaces, letting you
 easily build Google functionality into your applications
 
By default, gRPC uses Protocol Buffers, Google’s mature open source mechanism for serializing structured data
(although it can be used with other data formats such as JSON).

The first step when working with protocol buffers is to define the structure for the data you want
to serialize in a proto file: this is an ordinary text file with a .proto extension.
Protocol buffer data is structured as messages, where each message is a small logical
record of information containing a series of name-value pairs called fields. Here’s a simple example:

message Person {
  string name = 1;
  int32 id = 2;
  bool has_ponycopter = 3;
}

Then, once you’ve specified your data structures, you use the protocol buffer compiler protoc
to generate data access classes in your preferred language(s) from your proto definition.
These provide simple accessors for each field, like name() and set_name(), as well as methods
to serialize/parse the whole structure to/from raw bytes. So, for instance, if your chosen
language is C++, running the compiler on the example above will generate a class called Person.
You can then use this class in your application to populate, serialize, and retrieve Person protocol buffer messages.

You define gRPC services in ordinary proto files, with RPC method parameters and return
types specified as protocol buffer messages:

// The greeter service definition.
service Greeter {
  // Sends a greeting
  rpc SayHello (HelloRequest) returns (HelloReply) {}
}

// The request message containing the user's name.
message HelloRequest {
  string name = 1;
}

// The response message containing the greetings
message HelloReply {
  string message = 1;
}

gRPC uses protoc with a special gRPC plugin to generate code from your proto file:
you get generated gRPC client and server code, as well as the regular protocol buffer
code for populating, serializing, and retrieving your message types


Service definition:
Like many RPC systems, gRPC is based around the idea of defining a service,
specifying the methods that can be called remotely with their parameters and return types.
By default, gRPC uses protocol buffers as the Interface Definition Language (IDL) for
describing both the service interface and the structure of the payload messages.
It is possible to use other alternatives if desired.

service HelloService {
  rpc SayHello (HelloRequest) returns (HelloResponse);
}

message HelloRequest {
  string greeting = 1;
}

message HelloResponse {
  string reply = 1;
}
gRPC lets you define four kinds of service method:

1. Unary RPCs: where the client sends a single request to the server and gets
 a single response back, just like a normal function call.

rpc SayHello(HelloRequest) returns (HelloResponse);

2. Server streaming RPCs: where the client sends a request to the server and gets a stream
 to read a sequence of messages back. The client reads from the returned stream until there are no more messages.
  gRPC guarantees message ordering within an individual RPC call.

rpc LotsOfReplies(HelloRequest) returns (stream HelloResponse);

3. Client streaming RPCs: where the client writes a sequence of messages and sends them to the server,
 again using a provided stream. Once the client has finished writing the messages,
 it waits for the server to read them and return its response.
 Again gRPC guarantees message ordering within an individual RPC call.

rpc LotsOfGreetings(stream HelloRequest) returns (HelloResponse);

4. Bidirectional streaming RPCs: where both sides send a sequence of messages using a read-write stream.
 The two streams operate independently, so clients and servers can read and write in whatever order
 they like: for example, the server could wait to receive all the client messages before writing its responses,
  or it could alternately read a message then write a message, or some other combination of reads and writes. The order of messages in each stream is preserved.

rpc BidiHello(stream HelloRequest) returns (stream HelloResponse);


Using the API:
Starting from a service definition in a .proto file, gRPC provides protocol buffer
compiler plugins that generate client- and server-side code. gRPC users typically call these 
APIs on the client side and implement the corresponding API on the server side.

On the server side:, the server implements the methods declared by the service and runs a gRPC server
to handle client calls. The gRPC infrastructure decodes incoming requests,
executes service methods, and encodes service responses.

On the client side:, the client has a local object known as stub (for some languages, the preferred term is client)
that implements the same methods as the service. The client can then just call those methods
on the local object, wrapping the parameters for the call in the appropriate protocol
buffer message type - gRPC looks after sending the request(s) to the server and returning the server’s
protocol buffer response(s).

Synchronous vs. asynchronous:
Synchronous RPC calls that block until a response arrives from the server are the closest
approximation to the abstraction of a procedure call that RPC aspires to. On the other hand,
networks are inherently asynchronous and in many scenarios it’s useful to be able to start RPCs
without blocking the current thread.
The gRPC programming API in most languages comes in both synchronous and asynchronous flavors.
You can find out more in each language’s tutorial and reference documentation
(complete reference docs are coming soon).

RPC life cycle:
what happens when a gRPC client calls a gRPC server method. For complete implementation details,
see the language-specific pages.  https://grpc.io/docs/languages/python/quickstart/

Unary RPC:
First consider the simplest type of RPC where the client sends a single request and gets back a single response.

Once the client calls a stub method, the server is notified that the RPC has been invoked with the client’s metadata
for this call, the method name, and the specified deadline if applicable.
The server can then either send back its own initial metadata (which must be sent before any response) straight away,
or wait for the client’s request message. Which happens first, is application-specific.
Once the server has the client’s request message, it does whatever work is necessary to create and populate a response. The response is then returned (if successful) to the client together with status details (status code and optional status message) and optional trailing metadata.
If the response status is OK, then the client gets the response, which completes the call on the client side.
Server streaming RPC

A server-streaming RPC:  is similar to a unary RPC, except that the server returns a stream of messages
in response to a client’s request. After sending all its messages, the server’s status details
(status code and optional status message) and optional trailing metadata are sent to the client.
This completes processing on the server side. The client completes once it has all the server’s messages.

Client streaming RPC:
A client-streaming RPC is similar to a unary RPC, except that the client sends a stream of messages
to the server instead of a single message. The server responds with a single message (along with its status
details and optional trailing metadata), typically but not necessarily after it has received all the
client’s messages.

Bidirectional streaming RPC:
In a bidirectional streaming RPC, the call is initiated by the client invoking the method
and the server receiving the client metadata, method name, and deadline. The server can choose to send back
its initial metadata or wait for the client to start streaming messages.

Client- and server-side stream processing is application specific. 
Since the two streams are independent, the client and server can read and write messages 
in any order. For example, a server can wait until it has received all of a client’s messages 
before writing its messages, or the server and client can play “ping-pong” – the server gets a request,
then sends back a response, then the client sends another request based on the response, and so on.

Deadlines/Timeouts:
gRPC allows clients to specify how long they are willing to wait for an RPC to complete
before the RPC is terminated with a DEADLINE_EXCEEDED error. On the server side, the server 
can query to see if a particular RPC has timed out, or how much time is left to complete the RPC.

Specifying a deadline or timeout is language specific: some language APIs work in terms of timeouts 
(durations of time), and some language APIs work in terms of a deadline (a fixed point in time)
 and may or may not have a default deadline.

RPC termination:
In gRPC, both the client and server make independent and local determinations
of the success of the call, and their conclusions may not match. This means that,
for example, you could have an RPC that finishes successfully on the server side 
(“I have sent all my responses!”) but fails on the client side
(“The responses arrived after my deadline!”). It’s also possible for a server to decide 
to complete before a client has sent all its requests.

Cancelling an RPC:
Either the client or the server can cancel an RPC at any time. 
A cancellation terminates the RPC immediately so that no further work is done.
Warning: Changes made before a cancellation are not rolled back.

Metadata: Metadata is information about a particular RPC call (such as authentication details)
in the form of a list of key-value pairs, where the keys are strings and the values are typically strings,
but can be binary data. Metadata is opaque to gRPC itself - it lets the client provide
information associated with the call to the server and vice versa.

Access to metadata is language dependent.

Channels:
A gRPC channel provides a connection to a gRPC server on a specified host and port.
It is used when creating a client stub. Clients can specify channel arguments to modify gRPC’s default behavior,
such as switching message compression on or off. A channel has state, including connected and idle.

How gRPC deals with closing a channel is language dependent. Some languages also permit querying channel state.


Prerequisites
Python 3.5 or higher
pip version 9.0.1 or higher
If necessary, upgrade your version of pip:

$ python -m pip install --upgrade pip
If you cannot upgrade pip due to a system-owned installation, you can run the example in a virtualenv:

$ python -m pip install virtualenv
$ virtualenv venv
$ source venv/bin/activate
$ python -m pip install --upgrade pip

Install gRPC:

$ python -m pip install grpcio
Or, to install it system wide:

$ sudo python -m pip install grpcio
gRPC tools
Python’s gRPC tools include the protocol buffer compiler protoc and the special plugin for generating
server and client code from .proto service definitions. For the first part of our quick-start example,
we’ve already generated the server and client stubs from helloworld.proto, but you’ll need the tools
 for the rest of our quick start, as well as later tutorials and your own projects.

To install gRPC tools, run:

$ python -m pip install grpcio-tools
Download the example
You’ll need a local copy of the example code to work through this quick start. Download the example code
from our GitHub repository (the following command clones the entire repository, but you just need the examples
for this quick start and other tutorials):

# Clone the repository to get the example code:
$ git clone -b v1.46.3 --depth 1 --shallow-submodules https://github.com/grpc/grpc
# Navigate to the "hello, world" Python example:
$ cd grpc/examples/python/helloworld
Run a gRPC application
From the examples/python/helloworld directory:

Run the server:

$ python greeter_server.py
From another terminal, run the client:

$ python greeter_client.py
Congratulations! You’ve just run a client-server application with gRPC.

Update the gRPC service
Now let’s look at how to update the application with an extra method on the
 server for the client to call. Our gRPC service is defined using protocol buffers;
you can find out lots more about how to define a service in a .proto file in Introduction 
to gRPC and Basics tutorial. For now all you need to know is that both the server and the client
“stub” have a SayHello RPC method that takes a HelloRequest parameter from the client and returns
a HelloReply from the server, and that this method is defined like this:

// The greeting service definition.
service Greeter {
  // Sends a greeting
  rpc SayHello (HelloRequest) returns (HelloReply) {}
}

// The request message containing the user's name.
message HelloRequest {
  string name = 1;
}

// The response message containing the greetings
message HelloReply {
  string message = 1;
}
Let’s update this so that the Greeter service has two methods.
Edit examples/protos/helloworld.proto and update it with a new SayHelloAgain method,
 with the same request and response types:

// The greeting service definition.
service Greeter {
  // Sends a greeting
  rpc SayHello (HelloRequest) returns (HelloReply) {}
  // Sends another greeting
  rpc SayHelloAgain (HelloRequest) returns (HelloReply) {}
}

// The request message containing the user's name.
message HelloRequest {
  string name = 1;
}

// The response message containing the greetings
message HelloReply {
  string message = 1;
}
Remember to save the file!

Generate gRPC code
Next we need to update the gRPC code used by our application to use the new service definition.

From the examples/python/helloworld directory, run:

$ python -m grpc_tools.protoc -I../../protos --python_out=. --grpc_python_out=. ../../protos/helloworld.proto
This regenerates helloworld_pb2.py which contains our generated request and response
classes and helloworld_pb2_grpc.py which contains our generated client and server classes.

Update and run the application
We now have new generated server and client code, but we still need to implement and call
 the new method in the human-written parts of our example application.

Update the server
In the same directory, open greeter_server.py. Implement the new method like this:

class Greeter(helloworld_pb2_grpc.GreeterServicer):

  def SayHello(self, request, context):
    return helloworld_pb2.HelloReply(message='Hello, %s!' % request.name)

  def SayHelloAgain(self, request, context):
    return helloworld_pb2.HelloReply(message='Hello again, %s!' % request.name)
...
Update the client
In the same directory, open greeter_client.py. Call the new method like this:

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = helloworld_pb2_grpc.GreeterStub(channel)
        response = stub.SayHello(helloworld_pb2.HelloRequest(name='you'))
        print("Greeter client received: " + response.message)
        response = stub.SayHelloAgain(helloworld_pb2.HelloRequest(name='you'))
        print("Greeter client received: " + response.message)
Run!
Just like we did before, from the examples/python/helloworld directory:

Run the server:

$ python greeter_server.py
From another terminal, run the client:

$ python greeter_client.py


https://grpc.io/docs/languages/python/basics/


a basic Python programmer’s introduction to working with gRPC.

By walking through this example you’ll learn how to:

Define a service in a .proto file.
Generate server and client code using the protocol buffer compiler.
Use the Python gRPC API to write a simple client and server for your service.
It assumes that you have read the Introduction to gRPC and are familiar with protocol buffers. You can find out more in the proto3 language guide and Python generated code guide.

Why use gRPC?
Our example is a simple route mapping application that lets clients get information about features on their route, create a summary of their route, and exchange route information such as traffic updates with the server and other clients.

With gRPC we can define our service once in a .proto file and generate clients and servers in any of gRPC’s supported languages, which in turn can be run in environments ranging from servers inside a large data center to your own tablet — all the complexity of communication between different languages and environments is handled for you by gRPC. We also get all the advantages of working with protocol buffers, including efficient serialization, a simple IDL, and easy interface updating.

Example code and setup
The example code for this tutorial is in grpc/grpc/examples/python/route_guide. To download the example, clone the grpc repository by running the following command:

$ git clone -b v1.46.3 --depth 1 --shallow-submodules https://github.com/grpc/grpc
Then change your current directory to examples/python/route_guide in the repository:

$ cd grpc/examples/python/route_guide
You also should have the relevant tools installed to generate the server and client interface code - if you don’t already, follow the setup instructions in Quick start.

Defining the service
Your first step (as you’ll know from the Introduction to gRPC) is to define the gRPC service and the method request and response types using protocol buffers. You can see the complete .proto file in examples/protos/route_guide.proto.

To define a service, you specify a named service in your .proto file:

service RouteGuide {
   // (Method definitions not shown)
}
Then you define rpc methods inside your service definition, specifying their request and response types. gRPC lets you define four kinds of service method, all of which are used in the RouteGuide service:

A simple RPC where the client sends a request to the server using the stub and waits for a response to come back, just like a normal function call.

// Obtains the feature at a given position.
rpc GetFeature(Point) returns (Feature) {}
A response-streaming RPC where the client sends a request to the server and gets a stream to read a sequence of messages back. The client reads from the returned stream until there are no more messages. As you can see in the example, you specify a response-streaming method by placing the stream keyword before the response type.

// Obtains the Features available within the given Rectangle.  Results are
// streamed rather than returned at once (e.g. in a response message with a
// repeated field), as the rectangle may cover a large area and contain a
// huge number of features.
rpc ListFeatures(Rectangle) returns (stream Feature) {}
A request-streaming RPC where the client writes a sequence of messages and sends them to the server, again using a provided stream. Once the client has finished writing the messages, it waits for the server to read them all and return its response. You specify a request-streaming method by placing the stream keyword before the request type.

// Accepts a stream of Points on a route being traversed, returning a
// RouteSummary when traversal is completed.
rpc RecordRoute(stream Point) returns (RouteSummary) {}
A bidirectionally-streaming RPC where both sides send a sequence of messages using a read-write stream. The two streams operate independently, so clients and servers can read and write in whatever order they like: for example, the server could wait to receive all the client messages before writing its responses, or it could alternately read a message then write a message, or some other combination of reads and writes. The order of messages in each stream is preserved. You specify this type of method by placing the stream keyword before both the request and the response.

// Accepts a stream of RouteNotes sent while a route is being traversed,
// while receiving other RouteNotes (e.g. from other users).
rpc RouteChat(stream RouteNote) returns (stream RouteNote) {}
Your .proto file also contains protocol buffer message type definitions for all the request and response types used in our service methods - for example, here’s the Point message type:

// Points are represented as latitude-longitude pairs in the E7 representation
// (degrees multiplied by 10**7 and rounded to the nearest integer).
// Latitudes should be in the range +/- 90 degrees and longitude should be in
// the range +/- 180 degrees (inclusive).
message Point {
  int32 latitude = 1;
  int32 longitude = 2;
}
Generating client and server code
Next you need to generate the gRPC client and server interfaces from your .proto service definition.

First, install the grpcio-tools package:

$ pip install grpcio-tools
Use the following command to generate the Python code:

$ python -m grpc_tools.protoc -I../../protos --python_out=. --grpc_python_out=. ../../protos/route_guide.proto
Note that as we’ve already provided a version of the generated code in the example directory, running this command regenerates the appropriate file rather than creates a new one. The generated code files are called route_guide_pb2.py and route_guide_pb2_grpc.py and contain:

classes for the messages defined in route_guide.proto
classes for the service defined in route_guide.proto
RouteGuideStub, which can be used by clients to invoke RouteGuide RPCs
RouteGuideServicer, which defines the interface for implementations of the RouteGuide service
a function for the service defined in route_guide.proto
add_RouteGuideServicer_to_server, which adds a RouteGuideServicer to a grpc.Server
Note
The 2 in pb2 indicates that the generated code is following Protocol Buffers Python API version 2. Version 1 is obsolete. It has no relation to the Protocol Buffers Language version, which is the one indicated by syntax = "proto3" or syntax = "proto2" in a .proto file.
Creating the server
First let’s look at how you create a RouteGuide server. If you’re only interested in creating gRPC clients, you can skip this section and go straight to Creating the client (though you might find it interesting anyway!).

Creating and running a RouteGuide server breaks down into two work items:

Implementing the servicer interface generated from our service definition with functions that perform the actual “work” of the service.
Running a gRPC server to listen for requests from clients and transmit responses.
You can find the example RouteGuide server in examples/python/route_guide/route_guide_server.py.

Implementing RouteGuide
route_guide_server.py has a RouteGuideServicer class that subclasses the generated class route_guide_pb2_grpc.RouteGuideServicer:

# RouteGuideServicer provides an implementation of the methods of the RouteGuide service.
class RouteGuideServicer(route_guide_pb2_grpc.RouteGuideServicer):
RouteGuideServicer implements all the RouteGuide service methods.

Simple RPC
Let’s look at the simplest type first, GetFeature, which just gets a Point from the client and returns the corresponding feature information from its database in a Feature.

def GetFeature(self, request, context):
  feature = get_feature(self.db, request)
  if feature is None:
    return route_guide_pb2.Feature(name="", location=request)
  else:
    return feature
The method is passed a route_guide_pb2.Point request for the RPC, and a grpc.ServicerContext object that provides RPC-specific information such as timeout limits. It returns a route_guide_pb2.Feature response.

Response-streaming RPC
Now let’s look at the next method. ListFeatures is a response-streaming RPC that sends multiple Features to the client.

def ListFeatures(self, request, context):
  left = min(request.lo.longitude, request.hi.longitude)
  right = max(request.lo.longitude, request.hi.longitude)
  top = max(request.lo.latitude, request.hi.latitude)
  bottom = min(request.lo.latitude, request.hi.latitude)
  for feature in self.db:
    if (feature.location.longitude >= left and
        feature.location.longitude <= right and
        feature.location.latitude >= bottom and
        feature.location.latitude <= top):
      yield feature
Here the request message is a route_guide_pb2.Rectangle within which the client wants to find Features. Instead of returning a single response the method yields zero or more responses.

Request-streaming RPC
The request-streaming method RecordRoute uses an iterator of request values and returns a single response value.

def RecordRoute(self, request_iterator, context):
  point_count = 0
  feature_count = 0
  distance = 0.0
  prev_point = None

  start_time = time.time()
  for point in request_iterator:
    point_count += 1
    if get_feature(self.db, point):
      feature_count += 1
    if prev_point:
      distance += get_distance(prev_point, point)
    prev_point = point

  elapsed_time = time.time() - start_time
  return route_guide_pb2.RouteSummary(point_count=point_count,
                                      feature_count=feature_count,
                                      distance=int(distance),
                                      elapsed_time=int(elapsed_time))
Bidirectional streaming RPC
Lastly let’s look at the bidirectionally-streaming method RouteChat.

def RouteChat(self, request_iterator, context):
  prev_notes = []
  for new_note in request_iterator:
    for prev_note in prev_notes:
      if prev_note.location == new_note.location:
        yield prev_note
    prev_notes.append(new_note)
This method’s semantics are a combination of those of the request-streaming method and the response-streaming method. It is passed an iterator of request values and is itself an iterator of response values.

Starting the server
Once you have implemented all the RouteGuide methods, the next step is to start up a gRPC server so that clients can actually use your service:

def serve():
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  route_guide_pb2_grpc.add_RouteGuideServicer_to_server(
      RouteGuideServicer(), server)
  server.add_insecure_port('[::]:50051')
  server.start()
  server.wait_for_termination()
The server start() method is non-blocking. A new thread will be instantiated to handle requests. The thread calling server.start() will often not have any other work to do in the meantime. In this case, you can call server.wait_for_termination() to cleanly block the calling thread until the server terminates.

Creating the client
You can see the complete example client code in examples/python/route_guide/route_guide_client.py.

Creating a stub
To call service methods, we first need to create a stub.

We instantiate the RouteGuideStub class of the route_guide_pb2_grpc module, generated from our .proto.

channel = grpc.insecure_channel('localhost:50051')
stub = route_guide_pb2_grpc.RouteGuideStub(channel)
Calling service methods
For RPC methods that return a single response (“response-unary” methods), gRPC Python supports both synchronous (blocking) and asynchronous (non-blocking) control flow semantics. For response-streaming RPC methods, calls immediately return an iterator of response values. Calls to that iterator’s next() method block until the response to be yielded from the iterator becomes available.

Simple RPC
A synchronous call to the simple RPC GetFeature is nearly as straightforward as calling a local method. The RPC call waits for the server to respond, and will either return a response or raise an exception:

feature = stub.GetFeature(point)
An asynchronous call to GetFeature is similar, but like calling a local method asynchronously in a thread pool:

feature_future = stub.GetFeature.future(point)
feature = feature_future.result()
Response-streaming RPC
Calling the response-streaming ListFeatures is similar to working with sequence types:

for feature in stub.ListFeatures(rectangle):
Request-streaming RPC
Calling the request-streaming RecordRoute is similar to passing an iterator to a local method. Like the simple RPC above that also returns a single response, it can be called synchronously or asynchronously:

route_summary = stub.RecordRoute(point_iterator)
route_summary_future = stub.RecordRoute.future(point_iterator)
route_summary = route_summary_future.result()
Bidirectional streaming RPC
Calling the bidirectionally-streaming RouteChat has (as is the case on the service-side) a combination of the request-streaming and response-streaming semantics:

for received_route_note in stub.RouteChat(sent_route_note_iterator):
Try it out!
Run the server:

$ python route_guide_server.py
From a different terminal, run the client:

$ python route_guide_client.py



ALTS authentication:
An overview of gRPC authentication in Python using Application Layer Transport Security (ALTS).

Overview
Application Layer Transport Security (ALTS) is a mutual authentication and transport encryption system developed by Google. It is used for securing RPC communications within Google’s infrastructure. ALTS is similar to mutual TLS but has been designed and optimized to meet the needs of Google’s production environments. For more information, take a look at the ALTS whitepaper.

ALTS in gRPC has the following features:

Create gRPC servers & clients with ALTS as the transport security protocol.
ALTS connections are end-to-end protected with privacy and integrity.
Applications can access peer information such as the peer service account.
Client authorization and server authorization support.
Minimal code changes to enable ALTS.
gRPC users can configure their applications to use ALTS as a transport security protocol with few lines of code.

Note that ALTS is fully functional if the application runs on Google Cloud Platform. ALTS could be run on any platforms with a pluggable ALTS handshaker service.

gRPC Client with ALTS Transport Security Protocol
gRPC clients can use ALTS credentials to connect to servers, as illustrated in the following code excerpt:

import grpc

channel_creds = grpc.alts_channel_credentials()
channel = grpc.secure_channel(address, channel_creds)
gRPC Server with ALTS Transport Security Protocol
gRPC servers can use ALTS credentials to allow clients to connect to them, as illustrated next:

import grpc

server = grpc.server(futures.ThreadPoolExecutor())
server_creds = grpc.alts_server_credentials()
server.add_secure_port(server_address, server_creds)