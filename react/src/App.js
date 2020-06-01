import React from 'react';
import './App.css';
import axios from 'axios'
import Home from './Component/home'
class App extends React.Component {
  state = {
    Selectedfile : null,
    predictedImage: null,
    previewImage: null,
    predictedMonetImage:null
  }

//   componentDidMount(){
//     axios.get('https://jsonplaceholder.typicode.com/photos')
//         .then((res)=>{
//             console.log(res.data[0].thumbnailUrl)
//             this.setState({
//               predictedImage:res.data[0].thumbnailUrl
//             })
//         })
// }
  fileSelectedHandler = event => {
    console.log(event.target.files[0])
    let file = event.target.files[0]
    if (file){
      this.setState({
        Selectedfile: file,
        previewImage: URL.createObjectURL(file)
      })
    }else{
      return
    }
  }

  fileUploadHandler = (e) => {
    const fd = new FormData()
    fd.append('file',this.state.Selectedfile,'download.png')
    axios.post('http://127.0.0.1:5000/monet_to_photo',fd).
      then(res=>{
        console.log(res)
            this.setState({
              predictedImage:'http://localhost:5000' + res.data
            })
      })
      
  }

   fileUploadImageHandler = (e) => {
    const fd = new FormData()
    fd.append('file',this.state.Selectedfile,'download.png')
    axios.post('http://127.0.0.1:5000/photo_to_monet',fd).
      then(res=>{
        console.log(res)
            this.setState({
              predictedMonetImage:'http://localhost:5000' + res.data
            })
      })

  }
  render(){
    return (
      <div className='app'>        
        <Home fileUploadHandler={this.fileUploadHandler} 
        fileSelectedHandler={this.fileSelectedHandler} 
        Selectedfile={this.state.Selectedfile}
        previewImage={this.state.previewImage}
        predictedImage={this.state.predictedImage}
        predictedMonetImage = {this.state.predictedMonetImage}
        fileUploadImageHandler={this.fileUploadImageHandler}/>
      </div>
    );
  }
  
}

export default App;
