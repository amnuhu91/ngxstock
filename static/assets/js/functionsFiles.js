const sendData=async(url,data)=>{
    console.log('url',url)
    console.log('payload Data',data)
    
    try {
     
      const res= await  axios.post(url,data)
      return res
    } catch (error) {
      console.log(error)
    }


  }


const sendGetRequest = async (url) =>{

}