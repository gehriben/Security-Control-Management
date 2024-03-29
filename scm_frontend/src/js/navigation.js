import * as React from "react";
import {
    BrowserRouter as Router,
    Routes,
    Route,
    Link
  } from "react-router-dom";

export default class Navigation extends React.Component {  
    render() {
      return (
        <div>
            <div id="mySidenav" class="sidenav">
                <div id="topSection">
                    <a href={`/`}>
                        <svg version="1.1" id="Capa_1" xmlns="http://www.w3.org/2000/svg" x="0px" y="0px" width="1em" height="1em" viewBox="0 0 201.865 201.865">
                        <g>
                            <path d="M200.65,105.892l-21.763-19.709V39.168c0-2.026-1.643-3.665-3.665-3.665h-19.158
                                c-0.973,0-1.908,0.383-2.598,1.074c-0.691,0.691-1.077,1.625-1.066,2.602l0.05,23.059l-47.466-42.993
                                c-1.389-1.256-3.482-1.267-4.889-0.032L1.247,106.278c-1.263,1.109-1.61,2.924-0.841,4.42c0.759,1.485,2.434,2.28,4.066,1.908
                                l21.971-4.96v67.758c-0.021,0.591-0.032,3.647,2.18,5.944c0.981,1.009,2.738,2.222,5.569,2.222c5.282,0,49.027-0.054,49.027-0.054
                                c2.029,0,3.661-1.643,3.665-3.665l0.057-40.509c-0.036-0.472,0.05-1.671,0.537-2.205c0.329-0.351,1.034-0.433,1.557-0.433h20.353
                                c0.913,0,2.147,0.147,2.781,0.805c0.698,0.716,0.687,1.961,0.676,2.154l-0.093,40.058c0,0.97,0.379,1.904,1.07,2.598
                                c0.687,0.687,1.632,1.081,2.598,1.081h48.003c3.264,0,5.268-1.378,6.363-2.527c2.559-2.663,2.473-6.313,2.459-6.564V106.54
                                l24.111,5.64c1.643,0.39,3.307-0.39,4.091-1.868C202.225,108.834,201.896,107.019,200.65,105.892z M159.744,42.836h11.817v36.705
                                l-11.76-10.651L159.744,42.836z M170.409,98.344c-1.081-0.258-2.24,0-3.11,0.698c-0.873,0.694-1.389,1.754-1.389,2.874v72.486
                                c0,0.394-0.143,1.12-0.419,1.403c-0.225,0.222-0.762,0.251-1.07,0.251h-44.328l0.079-36.129c0.032-0.44,0.218-4.366-2.609-7.401
                                c-1.356-1.435-3.858-3.153-8.181-3.153H89.029c-3.654,0-5.83,1.557-7.011,2.859c-2.516,2.788-2.473,6.524-2.409,7.573
                                l-0.057,36.383c-10.629,0.011-41.017,0.05-45.366,0.05c-0.132,0-0.215-0.007-0.268-0.007c-0.007,0-0.018,0-0.025,0
                                c-0.068-0.147-0.118-0.426-0.118-0.676v-72.493c0-1.113-0.515-2.169-1.381-2.867c-0.873-0.694-2.015-0.948-3.096-0.712
                                l-12.433,2.806l85.613-75.406l49.986,45.269v0.218h0.236l32.51,29.447L170.409,98.344z"/>
                        </g>
                        </svg> Dashboard </a>
                    <a href={`assets`}>
                        <svg version="1.1" id="Capa_1" xmlns="http://www.w3.org/2000/svg" x="0px" y="0px" width="1em" height="1em" viewBox="0 0 389.981 389.981">
                        <g>
                            <path d="M145.407,248.988l-2.775,26.209c-0.224,2.115,0.46,4.225,1.883,5.806c1.422,1.581,3.449,2.483,5.576,2.483h79.301
                                c2.126,0,4.153-0.903,5.576-2.483c1.422-1.581,2.106-3.691,1.883-5.806l-2.775-26.209h98.777c15.374,0,27.881-12.507,27.881-27.881
                                V27.881C360.733,12.507,348.225,0,332.852,0H40.63C25.256,0,12.749,12.507,12.749,27.881v193.226
                                c0,15.374,12.507,27.881,27.881,27.881H145.407z M221.055,268.487h-62.629l2.064-19.499h58.5L221.055,268.487z M40.63,15h292.222
                                c7.103,0,12.881,5.778,12.881,12.881V197.99H27.749V27.881C27.749,20.778,33.527,15,40.63,15z M27.749,221.107v-8.117h317.983
                                v8.117c0,7.103-5.778,12.881-12.881,12.881H40.63C33.527,233.988,27.749,228.21,27.749,221.107z"/>
                            <path d="M332.645,333.876c1.36-2.24,1.453-5.027,0.244-7.352l-14.813-28.499c-1.291-2.483-3.856-4.041-6.655-4.041H62.061
                                c-2.798,0-5.364,1.558-6.655,4.041l-14.813,28.499c-1.208,2.325-1.116,5.112,0.244,7.352s3.791,3.607,6.411,3.607h278.986
                                C328.854,337.484,331.285,336.116,332.645,333.876z M59.599,322.484l7.016-13.499h240.251l7.017,13.499H59.599z"/>
                            <path d="M345.733,350.982h-12c-17.368,0-31.499,14.13-31.499,31.499c0,4.142,3.358,7.5,7.5,7.5h59.997c4.142,0,7.5-3.358,7.5-7.5
                                C377.232,365.113,363.102,350.982,345.733,350.982z M319.04,374.981c2.735-5.337,8.295-8.999,14.693-8.999h12
                                c6.398,0,11.958,3.662,14.694,8.999H319.04z"/>
                        </g>
                        </svg> Assets </a>
                    <a href={`constraints`}>
                        <svg version="1.1" id="Capa_1" xmlns="http://www.w3.org/2000/svg" x="0px" y="0px" width="1em" height="1em" viewBox="0 0 247.574 247.574">
                        <g>
                            <path d="M123.787,0.001C55.53,0.001,0,55.531,0,123.787s55.53,123.786,123.787,123.786s123.787-55.53,123.787-123.786
                                S192.044,0.001,123.787,0.001z M123.787,232.573C63.802,232.573,15,183.772,15,123.787S63.802,15.001,123.787,15.001
                                s108.787,48.801,108.787,108.786S183.773,232.573,123.787,232.573z"/>
                            <path d="M133.047,123.786l42.316-58.429c2.43-3.355,1.68-8.044-1.675-10.474c-3.356-2.429-8.043-1.68-10.474,1.675L123.787,111
                                l-39.43-54.441c-2.43-3.356-7.12-4.105-10.474-1.675c-3.354,2.43-4.104,7.119-1.675,10.474l42.317,58.429l-42.317,58.43
                                c-2.43,3.355-1.68,8.044,1.675,10.474c1.33,0.963,2.868,1.426,4.394,1.426c2.322,0,4.613-1.076,6.08-3.101l39.43-54.442
                                l39.43,54.442c1.467,2.025,3.757,3.101,6.08,3.101c1.525,0,3.064-0.463,4.393-1.426c3.355-2.43,4.105-7.119,1.675-10.474
                                L133.047,123.786z"/>
                        </g>
                        </svg> Constraints </a>
                    <a href={`properties`}>
                        <svg version="1.1" id="Capa_1" xmlns="http://www.w3.org/2000/svg" x="0px" y="0px" width="1em" height="1em" viewBox="0 0 366.523 366.523">
                        <g>
                            <g>
                                <path d="M358.379,84.649c-1.666-3.766-5.078-6.469-9.125-7.228c-4.053-0.762-8.211,0.523-11.127,3.429l-46.148,45.966
                                    c-6.986,6.987-16.279,10.835-26.162,10.836c-9.881,0-19.172-3.848-26.16-10.837c-6.988-6.988-10.837-16.278-10.838-26.161
                                    c0-9.883,3.85-19.173,10.822-26.148l46.107-45.974c2.922-2.912,4.219-7.079,3.465-11.135c-0.754-4.056-3.461-7.479-7.232-9.146
                                    c-12.121-5.362-25.594-8.197-38.965-8.198c-24.838,0.001-47.881,9.362-64.879,26.361L162.939,41.61
                                    c-26.348,26.348-34.146,65.179-20.72,99.207L17.281,265.755C6.138,276.9,0.001,291.714,0,307.473
                                    c-0.001,15.759,6.136,30.574,17.279,41.719c11.145,11.144,25.961,17.279,41.719,17.279c15.759-0.001,30.574-6.137,41.719-17.279
                                    L225.668,224.24c10.719,4.191,22.238,6.379,33.797,6.379c24.705,0,47.93-9.619,65.396-27.088l15.195-15.194
                                    C366.678,161.714,374.039,120.046,358.379,84.649z M259.465,205.619c-10.801-0.002-21.477-2.541-31.002-7.481
                                    c-5.295-2.744-11.396-1.079-15.518,3.293L83.038,331.512c-6.422,6.423-14.96,9.958-24.041,9.958s-17.619-3.536-24.041-9.957
                                    c-6.42-6.422-9.957-14.959-9.957-24.04s3.537-17.619,9.959-24.041l130.06-129.925c4.485-4.262,6.041-10.226,3.294-15.521
                                    c-13.596-26.223-8.598-57.795,12.305-78.698l15.197-15.196c12.277-12.278,29.041-19.04,47.201-19.04
                                    c3.373,0,6.752,0.243,10.096,0.719l-31.135,31.045c-11.711,11.71-18.158,27.279-18.158,43.839
                                    c0.002,16.561,6.449,32.13,18.16,43.839c11.709,11.711,27.279,18.16,43.84,18.159c16.561-0.002,32.129-6.45,43.82-18.141
                                    l31.215-31.093c2.965,20.931-3.602,42.364-18.475,57.238l-15.195,15.196C294.438,198.598,277.49,205.619,259.465,205.619z"/>
                                <path d="M61.894,285.078c-5.209,0-10.106,2.027-13.789,5.711c-3.682,3.684-5.711,8.58-5.711,13.789s2.028,10.104,5.711,13.789
                                    c3.683,3.683,8.58,5.711,13.789,5.711c5.209-0.002,10.105-2.028,13.789-5.713c3.684-3.683,5.711-8.58,5.711-13.787
                                    c0-5.209-2.028-10.106-5.711-13.789C71.999,287.104,67.103,285.078,61.894,285.078z"/>
                            </g>
                        </g>
                        </svg> Properties </a>
                    <a href={`controls`}>
                        <svg version="1.1" id="Capa_1" xmlns="http://www.w3.org/2000/svg" x="0px" y="0px" width="1em" height="1em" viewBox="0 0 247.574 247.574">
                            <g>
                                <path d="M123.787,0.001C55.53,0.001,0,55.531,0,123.787s55.53,123.786,123.787,123.786s123.787-55.53,123.787-123.786
                                    S192.044,0.001,123.787,0.001z M123.787,232.573C63.802,232.573,15,183.772,15,123.787S63.802,15.001,123.787,15.001
                                    s108.787,48.801,108.787,108.786S183.773,232.573,123.787,232.573z"/>
                                <path d="M133.047,123.786l42.316-58.429c2.43-3.355,1.68-8.044-1.675-10.474c-3.356-2.429-8.043-1.68-10.474,1.675L123.787,111
                                    l-39.43-54.441c-2.43-3.356-7.12-4.105-10.474-1.675c-3.354,2.43-4.104,7.119-1.675,10.474l42.317,58.429l-42.317,58.43
                                    c-2.43,3.355-1.68,8.044,1.675,10.474c1.33,0.963,2.868,1.426,4.394,1.426c2.322,0,4.613-1.076,6.08-3.101l39.43-54.442
                                    l39.43,54.442c1.467,2.025,3.757,3.101,6.08,3.101c1.525,0,3.064-0.463,4.393-1.426c3.355-2.43,4.105-7.119,1.675-10.474
                                    L133.047,123.786z"/>
                            </g>
                        </svg> Controls </a>
                    <a href={`tags`}>
                        <svg version="1.1" id="Capa_1" xmlns="http://www.w3.org/2000/svg" x="0px" y="0px" width="1em" height="1em" viewBox="0 0 247.574 247.574">
                            <g>
                                <path d="M123.787,0.001C55.53,0.001,0,55.531,0,123.787s55.53,123.786,123.787,123.786s123.787-55.53,123.787-123.786
                                    S192.044,0.001,123.787,0.001z M123.787,232.573C63.802,232.573,15,183.772,15,123.787S63.802,15.001,123.787,15.001
                                    s108.787,48.801,108.787,108.786S183.773,232.573,123.787,232.573z"/>
                                <path d="M133.047,123.786l42.316-58.429c2.43-3.355,1.68-8.044-1.675-10.474c-3.356-2.429-8.043-1.68-10.474,1.675L123.787,111
                                    l-39.43-54.441c-2.43-3.356-7.12-4.105-10.474-1.675c-3.354,2.43-4.104,7.119-1.675,10.474l42.317,58.429l-42.317,58.43
                                    c-2.43,3.355-1.68,8.044,1.675,10.474c1.33,0.963,2.868,1.426,4.394,1.426c2.322,0,4.613-1.076,6.08-3.101l39.43-54.442
                                    l39.43,54.442c1.467,2.025,3.757,3.101,6.08,3.101c1.525,0,3.064-0.463,4.393-1.426c3.355-2.43,4.105-7.119,1.675-10.474
                                    L133.047,123.786z"/>
                            </g>
                        </svg> Tags </a>
                </div>
                <div id="bottomSection">
                    <hr class="solid"></hr>
                    <a href="">
                        <svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-gear-fill" fill="#181B12" xmlns="http://www.w3.org/2000/svg">
                            <path fill-rule="evenodd" d="M9.405 1.05c-.413-1.4-2.397-1.4-2.81 0l-.1.34a1.464 1.464 0 0 1-2.105.872l-.31-.17c-1.283-.698-2.686.705-1.987 1.987l.169.311c.446.82.023 1.841-.872 2.105l-.34.1c-1.4.413-1.4 2.397 0 2.81l.34.1a1.464 1.464 0 0 1 .872 2.105l-.17.31c-.698 1.283.705 2.686 1.987 1.987l.311-.169a1.464 1.464 0 0 1 2.105.872l.1.34c.413 1.4 2.397 1.4 2.81 0l.1-.34a1.464 1.464 0 0 1 2.105-.872l.31.17c1.283.698 2.686-.705 1.987-1.987l-.169-.311a1.464 1.464 0 0 1 .872-2.105l.34-.1c1.4-.413 1.4-2.397 0-2.81l-.34-.1a1.464 1.464 0 0 1-.872-2.105l.17-.31c.698-1.283-.705-2.686-1.987-1.987l-.311.169a1.464 1.464 0 0 1-2.105-.872l-.1-.34zM8 10.93a2.929 2.929 0 1 0 0-5.86 2.929 2.929 0 0 0 0 5.858z"/>
                        </svg> Settings
                    </a>
                </div>
            </div>
            <div class="topnav">
                <span class="Title">
                    Security Control Management
                </span>
            </div>
        </div>
      );
    }
  }