import React from "react";
import { Link } from "react-router-dom";
import Header from "../components/Header";
import homeStore from "../stores/homeStore";
import ListItem from "../components/Listitem";
export default function Home(){
    const store=homeStore();
    React.useEffect(()=>{
        store.fetchCoins();
    },[]);
    return(
        <div>
            <Header />
            <header className="home-search">
                <div className="width">
                    <h2>Search for a coin</h2>
                    <div className="home-search-input">
                        <input type="text" value={store.query} onChange={store.setQuery}/>
                    </div>
                </div>
            </header>
            <div className="home-cryptos"> 
                <div className="width">
                    <h2>Trending Coins</h2>
                    <div class="home-cryptos-list">
                    {store.coins.map((coin)=>{
                        return(
                        <ListItem key={coin.id} coin={coin} />
                        );
                    })}
                    </div>
                </div> 
            </div>
        </div>
    );
}