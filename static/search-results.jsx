// class ResultMap extends React.Component {
//     constructor(props) {
//         super(props);
//         this.googleMapRef = React.createRef();
//         }

//     componentDidMount() {
//         const googleMapScript = document.createElement('script')
//         googleMapScript.src =
//         `https://maps.googleapis.com/maps/api/js?key=AIzaSyAjzcFuaU59MQFb9_uODWbobJDnQ3Zm_A0`
//         window.document.body.appendChild(googleMapScript);

//         googleMapScript.addEventListener("load", () => {
//             this.googleMap = this.initMap();
//             this.createMarkers();
//         });
//     }

//     initMap = () =>
//         new window.google.maps.Map(this.googleMapRef.current, {
//             zoom: 12,
//             center: {
//                 lat: 37.7887459,
//                 lng: -122.4115852
//             },
//         });

//     createMarkers = () => {

//             let locations = [];
//             for (const place of this.props.places){
//                 let marker = place
//                 marker.coords.lat = parseFloat(marker.coords.lat);
//                 marker.coords.lng = parseFloat(marker.coords.lng);
//                 locations.push(marker);
//             };
//             console.log(locations)

//             const markers = [];
//             for (const location of locations) {
//                 markers.push(new window.google.maps.Marker({
//                     position: location.coords,
//                     title: location.name,
//                     map: this.googleMap,
//                     icon: {
//                         url: '/static/marker.svg',
//                         scaledSize: {
//                             width: 30,
//                             height: 30
//                         }
//                     }
//                 }));
//             }

//             for (const marker of markers) {
//                 const markerInfo = (`
//                   <h3>${marker.title}</h3>
//                   <p>
//                     Located at: <code>${marker.position.lat()}</code>,
//                     <code>${marker.position.lng()}</code>
//                   </p>
//                 `);

//                 const infoWindow = new google.maps.InfoWindow({
//                     content: markerInfo,
//                     maxWidth: 200
//                 });

//                 marker.addListener("click", () => {
//                     infoWindow.open(this.googleMap, marker);
//                 });

//             }
//     }


//     render(){

//         return (
//             <div
//               id="map"
//               ref={this.googleMapRef}
//               style={{ width: '800px', height: '600px' }}
//             />
//             )
//     }
// }

class EventTile extends React.Component {
    constructor(props){
        super(props)
    }

    render(){
        const saveButton = <SaveButton event={this.props.event_data} />
        return(
            <div className="event-tile">
                <a href={this.props.url}>{this.props.event_name}</a>
                <span>
                {this.props.user && saveButton}
                </span>
            </div>
            )
    }
}

class SaveButton extends React.Component {
    constructor(props){
        super(props)
        this.state = { saved: false }
    }

    render(){

        return(
            <button className="save-btn"
                id={ this.props.event.eventbrite_id }
                name={ this.props.event.eventbrite_id }
                value={ this.props.event }>Save Event</button>
            );
    }
}

class EventList extends React.Component {
    constructor(props){
        super(props)
    }

    render(){
        const resultList = [];

        for (const currentResult of this.props.results) {
            resultList.push(
                <EventTile key={currentResult.eventbrite_id}
                url={currentResult.event_url}
                event_name={currentResult.name}
                event_data={currentResult}
                user={this.props.user}
                />
            );
        }

        return(<div id="results">{resultList}</div>)
    }
}

class PageContainer extends React.Component {
    constructor(props){
        super(props);

        this.state = { events: [],
                       markers: [],
                       user: null }
        this.updateResults = this.updateResults.bind(this);
    }

    getResults = () => {
        $.get('/test.json', this.updateResults)
    }

    updateResults(response) {
        const events = response.results;
        const markers = response.markers;
        const user = response.user_id
        this.setState({ events: events,
                        markers: markers,
                        user: user });
        console.log(this.state)
    }

    componentDidMount() {
        this.getResults();
    }

    render(){

        return(
            <div>
            <EventList results={this.state.events} user={this.state.user} />
            </div>
            )
    }
}

ReactDOM.render(<PageContainer />, document.getElementById('container'))