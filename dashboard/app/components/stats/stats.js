import css from "./css.module.css"
import { CantidadPersonas } from "./cantidadPersonas"
import { TipoTicket } from "./tipoTicket"


const Stats = () => {
    return <div className={css.main}>
        <div className={css.grafico}>
            <TipoTicket />
            <CantidadPersonas />
        </div>
    </div> 
}

export { 
    Stats
}