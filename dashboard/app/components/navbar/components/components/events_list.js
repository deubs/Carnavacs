"use client"
import css from "@/app/styles/events_list.module.css"
import { store_events_list } from "@/app/stores/events_list"

import Event_li from "@/app/components/navbar/components/components/components/events_li"
import { Error } from "@/app/components/common/Error"
import { Loading } from "@/app/components/common/Loading"

export default function Events_list () {
    const { events_list } = store_events_list()
    
    return <div className={css.main}>
        {
            events_list == "loading" ? <Loading /> :
            events_list == "error" ? <Error /> :
            events_list.map((item, index) => <Event_li key={`e_li${index}`} data={item} />)
        }
    </div>
}
