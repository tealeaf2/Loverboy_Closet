import httpInstane  from "@/utils/http";

export function getSomething(){
    return httpInstane({
        url: '/api/posts'
    })
}