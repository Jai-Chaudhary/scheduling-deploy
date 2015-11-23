import React from 'react/addons';
import request from 'superagent-bluebird-promise';

import {step} from '../lib/constant';

export default React.createClass({
  mixins: [React.addons.LinkedStateMixin],
  getInitialState() {
    return { dateTime: '2014-09-27 12:30:15'};
  },
  handleGo() {
    request.post('/get_state')
      .send({time: this.state.dateTime}).then(
        res => {
          const state = res.body;
          return request.post('/evaluate_optimize').send(state).promise();
        }
        ).then(
          res => {
            return this.props.handleToAnimation(res.body);
          });
  },
  render() {
    return (
      <div>
        <h1>Config</h1>

        <div>
          <button onClick={this.handleGo}>Go</button>
          <br />
          <input type="text" valueLink={this.linkState('dateTime')} />
        </div>

      </div>
    );
  }
});
