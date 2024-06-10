import { writable } from "svelte/store";
import { browser } from "$app/environment";

const stored_access_token = browser ? localStorage.getItem('access_token') : undefined;
export const access_token = writable(stored_access_token);
access_token.subscribe(value => {
    if (!browser || !value)
        return ;
    localStorage.setItem('access_token', value['access_token']);
    localStorage.setItem('token_type', value['token_type']);
})