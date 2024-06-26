import service from "@/utils/request";

export function findDataSetByUserId(id) {
    return service({
        url: '/dataSet',
        method: 'get',
           params: {
            uid: id
        }
    })
}
export function deleteById(id) {
    return service({
        url: '/dataSet',
        method: 'delete',
           data: {
            id: id
        }
    })
}

export function addDateSet(data) {
    return service({
        url: '/dataSet',
        method: 'post',
        data: data,
        headers: {
            'Content-Type': 'multipart/form-data'
          },
    })
}