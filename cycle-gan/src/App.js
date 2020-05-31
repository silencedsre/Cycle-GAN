import React from 'react';
import './App.css';
import axios from 'axios'
import Home from './Component/home'
class App extends React.Component {
  state = {
    Selectedfile : null,
    predictedImage: null
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
        Selectedfile: URL.createObjectURL(file)
      })
    }else{
      return
    }
  }

  fileUploadHandler = () => {
    const fd = new FormData()
    fd.append('file',this.state.Selectedfile, this.state.Selectedfile.name)
    axios.post('http://127.0.0.1:5000/monet_to_photo',fd).
      then(res=>{
        console.log(res)
            this.setState({
              predictedImage:res
            })
      })
      
  }
  render(){
    return (
      <div className='app'>        
        <Home fileUploadHandler={this.fileUploadHandler} 
        fileSelectedHandler={this.fileSelectedHandler} 
        Selectedfile={this.state.Selectedfile}
        predictedImage={this.state.predictedImage}/>
      </div>
    );
  }
  
}

export default App;
