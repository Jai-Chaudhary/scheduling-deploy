import React from 'react/addons';
import lodash from 'lodash';

import {avgStat, toTime, ganttHelper} from '../lib/util';

function statDiv(stats) {
  return <div>
    Avg waiting time: {avgStat(stats.wait)} <br/>
    Total waiting time: {lodash.sum(stats.wait)} <br/>
    {lodash.map(stats.siteWait,
        (wt, s) => <div key={s}>{s} avg waiting time: {lodash.round(wt)}</div>)}
    <br />
    {lodash.map(stats.overTime,
        (ot, s) => <div key={s}>{s} overtime: {ot}</div>)}
    Total overtime: {lodash.sum(stats.overTime)}
  </div>;
}

export default React.createClass({
  render() {
    const frame = this.props.frame;

    console.log(frame);
    const diversions = frame.diversionMetrics.map(d =>
        <div key={d.diversion.patient + d.diversion.site}>
          {d.diversion.patient} {d.diversion.site}
          {statDiv(d.stat)}
        </div>
    );

    return (
        <div>
          <h1>Animation</h1>
          <button onClick={this.props.handleToConfig}>Go Config</button>

          {statDiv(frame.stats)}

          {ganttHelper(frame.time, frame.animation, frame.stats)}

          <div>
          {diversions}
          </div>
        </div>
    );
  }
});
