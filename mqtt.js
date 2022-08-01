const mqtt = require('mqtt')
const spawn = require('child_process').spawn;
const createLoginMessage = require('./loginMessage')

const options = {
    host: '127.0.0.1',
    port: 1883
  };
  
  const client = mqtt.connect(options);
  client.subscribe("loginCheck")
  console.log('client.publish(loginCamera, ok)')
  client.publish('loginCamera', 'ok')

  client.on('message', (topic, message, packet) => {
    console.log("message is "+ message);
    console.log("topic is "+ topic);
    
    if(topic == "loginCheck"){
      console.log("topic == loginCheck")
      createLoginMessage(message)
    }
  })



module.exports = client

// client.subscribe('distance_closer');
// client.subscribe('distance_far');

// 

// client.on('message', function(topic, message){
//     if(topic.toString() == 'distance_closer'){
//         console.log(message.toString())

//         // const result = spawn('python', ['createAccount.py']);
//         // result.stdout.on('data', function(data) {
//         //     console.log(data.toString());
//         // });
//     }
//     else if(topic.toString() == 'distance_far'){
        
//     }
// });