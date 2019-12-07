const ActivityTile = (props) => {
    return (
            <div className="container justify-content-center align-items-center">
            <h1 className="display-4">{props.suggestion}</h1>
            <p className="lead">{props.description}</p>
            </div>
            );
}

const ChoiceButton = (props) => {
    return(
            <button onClick={props.function}>{props.name}</button>
        )
}


class ActivityPageContainer extends React.Component{
    constructor(props){
    super(props);

    this.state = { activity: 'Go to the Library',
                   description: 'Check Out Some Books'}
    this.newActivity = this.newActivity.bind(this);
}

getActivity = () => {
    $.get('/activities.json', this.newActivity)
}

newActivity(response) {
    const activity = response.activity;
    const description = response.description;
    this.setState({ activity: activity, description: description});
}

render() {

    return(
        <div className="jumbotron text-center">
        <ActivityTile suggestion={this.state.activity}
        description={this.state.description} newActivity={this.newActivity} />
        <ChoiceButton function={this.getActivity} name="New Choice Test" />
        </div>)
}

}

ReactDOM.render(<ActivityPageContainer />, document.getElementById('root'))