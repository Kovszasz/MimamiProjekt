import axios from 'axios';
import * as nsfwjs from 'nsfwjs'


async function predict(image){
  const model = await nsfwjs.load()
  const predictions = await model.classify(image, 5)
  return predictions
}
export default function (url, file,payload={}, multiple=true,name = 'img') {
  if (typeof url !== 'string') {
    throw new TypeError(`Expected a string, got ${typeof url}`);
  }
      predict(file.imageObject)


let token = localStorage.getItem('access_token');
  // You can add checks to ensure the url is valid, if you wish
console.log("img upload")
  const formData = new FormData();
  if (multiple){
    for(var i=0;i< file.length;i++){
      formData.append(name+String(i), file[i].file);
    }
  }else{
      formData.append(name, file);
  }
  for(var key in payload){
    formData.append(key,payload[key])
  }
  const config = {
    headers: {
      'content-type': 'multipart/form-data',
      'Authorization': `JWT ${ token }`

    }
  };
  return axios.post(url, formData, config);
}
