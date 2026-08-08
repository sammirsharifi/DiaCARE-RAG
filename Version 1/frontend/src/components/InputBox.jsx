import {
    useState,
    useRef
} from "react";


export default function InputBox({

    onSend

}) {


    const [text,setText] = useState("");

    const textareaRef = useRef();



    function send(){


        if(!text.trim())
            return;


        onSend(text);


        setText("");


        textareaRef.current.style.height="auto";


    }




    function handleChange(e){

        setText(e.target.value);


        e.target.style.height="auto";


        e.target.style.height =
            e.target.scrollHeight + "px";

    }



    return (

        <div className="input-container">


            <textarea

                ref={textareaRef}

                value={text}

                placeholder="Message Explainable GraphRAG..."

                onChange={handleChange}


                onKeyDown={(e)=>{


                    if(
                        e.key==="Enter"
                        &&
                        !e.shiftKey
                    ){

                        e.preventDefault();

                        send();

                    }

                }}


            />



            <button
                onClick={send}
            >

                ↑

            </button>



        </div>

    );

}