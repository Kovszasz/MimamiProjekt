import axios from 'axios';

export default function (url, file,payload={}, multiple=true,name = 'img') {
  if (typeof url !== 'string') {
    throw new TypeError(`Expected a string, got ${typeof url}`);
  }

  // You can add checks to ensure the url is valid, if you wish

  const formData = new FormData();
  if (multiple){
    console.log(file)
    console.log(file.length)
    for(var i=0;i< file.length;i++){
      console.log(file[i])
      console.log(file)
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
      'content-type': 'multipart/form-data'
    }
  };
  return axios.post(url, formData, config);
}
