import Typewriter from "./Typewriter";


export default function EvidencePanel({

    data

}) {


    if(!data)
        return null;



    const evidenceText =

        typeof data === "string"

        ?

        data

        :

        JSON.stringify(
            data,
            null,
            2
        );



    return (

        <div className="evidence-box">


            <div className="evidence-title">

                Evidence

            </div>



            <div className="evidence-text">


                <Typewriter

                    text={evidenceText}

                    speed={15}

                />


            </div>



        </div>

    );

}