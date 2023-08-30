import Head from 'next/head'

export const SiteMeta = () => {
  return (
    <Head>
      <title>216.show: Upcoming shows in Cleveland</title>
      <meta
        name='description'
        content='Concerts and events coming up at your fav local venues like the Beachland, Agora, Mahall’s, and more'
      />
      <meta name='viewport' content='width=device-width, initial-scale=1' />
      <link rel='icon' href='/favicon.png' />
    </Head>
  )
}
