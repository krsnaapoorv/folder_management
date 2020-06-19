import React from 'react'
import axios from 'axios'

class Folder extends React.Component{
    constructor(props){
        super(props)
        this.state = {
            data : [],
            val : 0,
            folder_name :""
        }
    }

    componentWillMount = () =>{
        axios.post('http://127.0.0.1:5000/showbelow',{
            "ancestor": 1
        })
        .then (res =>{
            console.log(res.data)
            this.setState({
                data : res.data.folders,
                val : res.data.value
            })
        }).catch(error => console.log(error))
    }

    show = (id) =>{
        // alert(id)
        axios.post('http://127.0.0.1:5000/showbelow',{
            "ancestor": id
        })
        .then (res =>{
            // console.log(res.data)
            this.setState({
                data : res.data.folders,
                val : res.data.value
            })
        }).catch(error => console.log(error))
    }

    back = () =>{
        if(this.state.val == 1){
            alert("Can't go back. This is root folder")
        }else{
            axios.post('http://127.0.0.1:5000/showabove',{
            "descendent": this.state.val
            })
            .then (res =>{
                // console.log(res.data)
                this.setState({
                    data : res.data.folders,
                    val : res.data.value
                })
            }).catch(error => console.log(error))
        }
        
    }

    add = () => {
        axios.post('http://127.0.0.1:5000/addfolder',{
            "folder_name": this.state.folder_name,
            "parent":this.state.val
        })
        .then (res =>{
            // console.log(res.data)
            alert(res.data.message)
            this.show(this.state.val)
        }).catch(error => console.log(error))
    }

    render() {
        return (
            <div className="container-fluid ">
                <button className="btn btn-secondary btn-lg mt-4" onClick={this.back}>Go Back</button>
                <div className="row">
                    <input type="text" className="form-control m-4 w-50" value = {this.state.folder_name} onChange={ (e) => this.setState({folder_name: e.target.value})} placeholder="Enter Folder Name" ></input>
                    <button className="btn btn-info btn m-4" onClick={this.add}>Add Folder</button>
                </div>
                <div className=" m-5 p-5 row justify-content-center bg-secondary">
                    {this.state.data.map(ele =>
                        <div className="mx-4">
                            <i className="far fa-3x fa-folder" onClick={()=> this.show(ele.id)} >{ele.folder_name}</i>
                        </div>
                    )}
                    <br></br>
                </div>
            </div>
        )
    }
}


export default Folder
