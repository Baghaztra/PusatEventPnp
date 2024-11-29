<template>
    <div class="d-flex align-items-center justify-content-center vh-100 bg-light">
        <div class="text-center">
            <h1 class="display-1 fw-bold">404</h1>
            <p class="fs-3"> <span class="text-danger">Opps!</span> Page not found. <i class="far fa-face-frown"></i> </p>
            <p class="lead">
                This might be because the event organizer's account has been disabled, <br>
                or the page you’re looking for doesn’t exist.
            </p>
            <router-link to="/home" class="btn btn-primary">Go Home</router-link>
        </div>
    </div>
</template>