import {
    useEffect,
    useState
} from "react";


export default function Typewriter({

    text,

    speed = 20

}) {


    const [display,setDisplay] =
        useState("");



    useEffect(() => {


        setDisplay("");

        let index = 0;



        const timer = setInterval(() => {


            setDisplay(

                text.slice(
                    0,
                    index + 1
                )

            );



            index++;



            if(index >= text.length){

                clearInterval(timer);

            }



        }, speed);



        return () =>
            clearInterval(timer);



    }, [text, speed]);



    return (

        <span>

            {display}

        </span>

    );

}