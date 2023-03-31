import React from 'react';
import {Link} from "react-router-dom";
export default function Header({back}){
    return (
       <header className="header">
        <div className="width">
            {back && (
                <Link to="/">
                <svg 
                    xmlns="http://www.w3.org/2000/svg" 
                    viewBox="0 0 48 48" 
                    width="24"
                >
                    <path 
                      fill="currentColor" 
                      d="M400 976 0 576l400-400 56 57-343 343 343 343-56 57Z"
                    />
                </svg>
                </Link>
            )}
            <h1>
                <Link to="/">Coiner!</Link>
            </h1>
        </div>
       </header>
    );
}