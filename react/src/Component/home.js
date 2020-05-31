import React from 'react'
import './home.css'
const Home = ({fileSelectedHandler,Selectedfile,fileUploadHandler,predictedImage}) =>{
    return(
        <div className='home'>
            <h2>Painting Generator</h2>
            <div className='image'>
                <div className='uploadedimage'>
                    <img className='img' src={Selectedfile} alt=''/>
                    <input className='input' type='file' onChange={fileSelectedHandler}/>

                </div>
                <div className='uploadedimage'>
                    <img className='img' src={predictedImage} alt=''/>
                    <div className='btn'>
                        <button onClick={fileUploadHandler}>Monet2Photo</button>
                        <button>Photo2Monet</button>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Home