import React from 'react/addons';

import Config from './Config';
import Animation from './Animation';

export default React.createClass({
  componentWillMount() {
    this.handleToConfig();
  },
  handleToAnimation(frame) {
    let e = <Animation handleToConfig={this.handleToConfig} frame={frame} />;
    this.setState({element: e});
  },
  handleToConfig() {
    let e = <Config handleToAnimation={this.handleToAnimation} />;
    this.setState({element: e});
  },
  render() {
    return this.state.element;
  }
});
